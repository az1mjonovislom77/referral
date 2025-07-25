import time
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import *

class SendPhoneView(APIView):
    def post(self, request):
        serializer = PhoneSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        code = f"{random.randint(1000, 9999)}"

        user, _ = User.objects.get_or_create(phone_number=phone)
        user.verification_code = code
        user.save()

        time.sleep(2)  # Simulate SMS sending delay
        print(f"Fake SMS code to {phone}: {code}")  # For testing

        return Response({"message": "Verification code sent."})

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = CodeVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.verification_code == code:
            user.is_verified = True
            user.save()
            return Response({"message": "User verified"})
        return Response({"error": "Invalid code"}, status=400)

class UserProfileView(APIView):
    def get(self, request):
        phone = request.query_params.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone, is_verified=True)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        return Response(UserProfileSerializer(user).data)

class ActivateInviteCodeView(APIView):
    def post(self, request):
        phone = request.data.get("phone_number")
        code = request.data.get("invite_code")

        try:
            user = User.objects.get(phone_number=phone, is_verified=True)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.used_invite_code:
            return Response({"message": "Invite code already used"}, status=400)

        if not User.objects.filter(invite_code=code).exists():
            return Response({"error": "Invite code does not exist"}, status=404)

        user.used_invite_code = code
        user.save()
        return Response({"message": "Invite code activated"})
