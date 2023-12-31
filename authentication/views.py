from random import randint
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from .serializers import (
    ResetPasswordSerializer,
    VerifyOTPSerializer,
    UpdatePasswordSerializer,
)
from .models import OTP, PasswordResetToken
from .utils import send_otp
from accounts.models import UserProfile
from secrets import token_hex as generateToken


class SendMailView(GenericAPIView):
    
    """
    Send OTP To Mail.

    Takes User Mail and send OTP to Verify it.
    """

    serializer_class = ResetPasswordSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["mail"]

            # Checking If Any OTP Exists For The Provided Mail
            old_otp = OTP.objects.filter(mail=email)

            # If OTP Exists Delete That OTP
            if old_otp:
                old_otp.delete()

            # Generate Random Six-Digit OTP
            otp = randint(1000, 9999)

            try:
                user = UserProfile.objects.get(email=email)

            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST
                )
            
            # Send OTP To Provided Mail
            if send_otp(otp, email) == 1:
                
                # If Email Sending is Succesful, Save OTP in Database And Return 200 Response
                expiry_time = timezone.now() + timezone.timedelta(minutes=5)
                OTP.objects.create(mail=email, otp=otp, expiry_time=expiry_time)

                return Response(
                    {"message": "Email sent successfully"}, status=status.HTTP_200_OK
                )
            else:

                # Email sending failed
                return Response(
                    {"message": "Email sending failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(GenericAPIView):

    """
    Verify OTP

    Takes User Mail and OTP And Verify Them.
    """

    serializer_class = VerifyOTPSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data["otp"]
            email = serializer.validated_data["mail"]

            # Check OTP from Database
            try:
                otp_object = OTP.objects.get(mail=email, otp=otp)

            except OTP.DoesNotExist:
                return Response(
                    {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Check If OTP Is Expired
            if otp_object.has_expired():
                return Response(
                    {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                )
            
            # Deleting Verified OTP
            otp_object.delete()

            # Removing Account If It Is Already Present In Verified Account Table
            password_reset_token = generateToken(32)
            expiry_time = timezone.now() + timezone.timedelta(minutes=5)

            try:
                user = UserProfile.objects.get(email=email)

            except:
                
                return Response(
                    {"error": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST
                )
            
            PasswordResetToken.objects.create(user=user,token=password_reset_token,expiry_time=expiry_time)
            
            return Response(
                {
                    "message": "OTP verified successfully",
                    "token" : password_reset_token
                }, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(GenericAPIView):

    """
    Change Password After Verifying Mail.

    Takes Verified Mail and New Password And Updates User Password.
    """

    serializer_class = UpdatePasswordSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]

            # Checking If User Is Verified Or Not
            try:
                verifyPasswordToken = PasswordResetToken.objects.get(token=token)

            except PasswordResetToken.DoesNotExist:

                return Response(
                    {"error": "User Verification Failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Checking If PasswordResetToken Is Expired
            if verifyPasswordToken.has_expired():
                verifyPasswordToken.delete()

                return Response(
                    {"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST
                )

            
            userObject = verifyPasswordToken.user

            # Set userPassword to password
            userObject.password = make_password(new_password)
            userObject.save()

            # Removing User Password Reset Token
            verifyPasswordToken.delete()

            return Response(
                {"message": "Password updated successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
