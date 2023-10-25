from rest_framework import serializers

class ResetPasswordSerializer(serializers.Serializer):
    mail = serializers.EmailField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    mail = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)


class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)