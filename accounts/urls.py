from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import path, reverse_lazy

from .forms import ResetPasswordSetForm
from .views import ForgotPasswordView, LoginView, LogoutView, SignUpView

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("sign-up/", SignUpView.as_view(), name="sign_up"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=ResetPasswordSetForm,
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
