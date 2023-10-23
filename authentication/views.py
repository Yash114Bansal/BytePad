from random import randint
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import (
    ResetPasswordSerializer,
    VerifyOTPSerializer,
    UpdatePasswordSerializer,
)
from .models import OTP, AllowPasswordReset
from .utils import send_otp
from accounts.models import UserProfile


class SendMailView(GenericAPIView):
    
    """
    Takes User Mail and send OTP to Verify it
    """

    serializer_class = ResetPasswordSerializer

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
            otp = randint(100000, 999999)

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
    Takes User Mail and OTP And Verify Them
    """

    serializer_class = VerifyOTPSerializer

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
            old_account = AllowPasswordReset.objects.filter(mail=email)

            if old_account:
                old_account.delete()

            # Creating New Object For Verified Account
            AllowPasswordReset.objects.create(mail=email)

            return Response(
                {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(GenericAPIView):

    """
    Takes Verified Mail and New Password And Updates User Password
    """

    serializer_class = UpdatePasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["mail"]
            new_password = serializer.validated_data["new_password"]

            # Checking If User Is Verified Or Not
            try:
                verifyUserObject = AllowPasswordReset.objects.get(mail=email)

            except AllowPasswordReset.DoesNotExist:
                return Response(
                    {"error": "User Verification Failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Checking If User Exits Or Not
            try:
                userObject = UserProfile.objects.get(email=email)

            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Set userPassword to password
            userObject.password = make_password(new_password)
            userObject.save()

            # Removing User From Verified User
            verifyUserObject.delete()

            return Response(
                {"message": "Password updated successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
