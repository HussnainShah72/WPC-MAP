from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import ForgotPasswordForm, LoginForm, SignUpForm


class RedirectAuthenticatedUserMixin:
    authenticated_redirect_url = reverse_lazy("core:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_authenticated_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_authenticated_redirect_url(self):
        return str(self.authenticated_redirect_url)


class LoginView(RedirectAuthenticatedUserMixin, FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "Welcome back.")
        return super().form_valid(form)


class SignUpView(RedirectAuthenticatedUserMixin, FormView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Your account has been created.")
        return super().form_valid(form)


class ForgotPasswordView(RedirectAuthenticatedUserMixin, FormView):
    template_name = "accounts/forgot_password.html"
    form_class = ForgotPasswordForm
    success_url = reverse_lazy("accounts:forgot_password")

    def form_valid(self, form):
        form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
        )
        messages.success(
            self.request,
            "If an account exists for that email, a reset link has been sent.",
        )
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")
