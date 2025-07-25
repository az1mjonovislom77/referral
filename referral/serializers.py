from rest_framework import serializers
from .models import User

class PhoneSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class CodeVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

class InviteActivateSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'used_invite_code', 'referrals']

    def get_referrals(self, obj):
        return [u.phone_number for u in obj.referrals()]
