from django.urls import path
from .views import *

urlpatterns = [
    path('send_code/', SendPhoneView.as_view()),
    path('verify_code/', VerifyCodeView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('activate_invite/', ActivateInviteCodeView.as_view()),
]
