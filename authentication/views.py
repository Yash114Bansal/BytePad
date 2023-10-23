from random import randint
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import ResetPasswordSerializer, VerifyOTPSerializer, UpdatePasswordSerializer
from .models import OTP, AllowPasswordReset
from .utils import send_otp
from accounts.models import UserProfile


class SendMailView(GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["mail"]
            old_otp = OTP.objects.filter(mail=email)

            if old_otp:
                old_otp.delete()

            otp = randint(100000, 999999)

            if send_otp(otp, email) == 1:
                expiry_time = timezone.now() + timezone.timedelta(minutes=5)
                OTP.objects.create(mail=email, otp=otp,
                                    expiry_time=expiry_time)

                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
            else:
                # Email sending failed
                return Response({"message": "Email sending failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(GenericAPIView):

    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            email = serializer.validated_data["mail"]

            try:
                otp_object = OTP.objects.get(mail=email, otp=otp)

            except OTP.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            if otp_object.has_expired():
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
            otp_object.delete()
            old_account = AllowPasswordReset.objects.filter(mail=email)

            if old_account:
                old_account.delete()

            AllowPasswordReset.objects.create(mail=email)

            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(GenericAPIView):

    serializer_class = UpdatePasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["mail"]
            new_password = serializer.validated_data['new_password']
            try:
                verifyUserObject = AllowPasswordReset.objects.get(mail=email)

            except AllowPasswordReset.DoesNotExist:
                return Response({'error': 'User Verification Failed'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                userObject = UserProfile.objects.get(email=email)

            except UserProfile.DoesNotExist:
                return Response({'error': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)

            #Set userPassword to password
            userObject.password = make_password(new_password)
            userObject.save()

            verifyUserObject.delete()

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)