from django.db import models
import random
import string

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True)
    used_invite_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            code = generate_invite_code()
            while User.objects.filter(invite_code=code).exists():
                code = generate_invite_code()
            self.invite_code = code
        super().save(*args, **kwargs)

    def referrals(self):
        return User.objects.filter(used_invite_code=self.invite_code)
