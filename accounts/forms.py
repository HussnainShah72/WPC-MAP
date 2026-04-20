from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password
User = get_user_model()


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-input")


class LoginForm(StyledFormMixin, forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Invalid login credentials",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"autocomplete": "email", "placeholder": "you@example.com"})
        self.fields["password"].widget.attrs.update({"autocomplete": "current-password"})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(self.request, username=email, password=password)
            if self.user is None:
                raise forms.ValidationError(self.error_messages["invalid_login"])
        return cleaned_data

    def get_user(self):
        return self.user


class SignUpForm(StyledFormMixin, forms.Form):
    admin_domain = "@insight.edu.au"

    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"autocomplete": "email", "placeholder": "you@example.com"})
        self.fields["password1"].widget.attrs.update({"autocomplete": "new-password"})
        self.fields["password2"].widget.attrs.update({"autocomplete": "new-password"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1:
            try:
                validate_password(password1)
            except forms.ValidationError as exc:
                self.add_error("password1", exc)

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match")

        return cleaned_data

    def save(self):
        email = self.cleaned_data["email"]
        is_admin_signup = email.lower().endswith(self.admin_domain)

        user = User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            role=User.Roles.ADMIN if is_admin_signup else User.Roles.VIEWER,
        )
        user.is_staff = is_admin_signup
        user.is_superuser = is_admin_signup
        user.save(update_fields=["is_staff", "is_superuser"])
        return user


class ForgotPasswordForm(StyledFormMixin, PasswordResetForm):
    email = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"autocomplete": "email", "placeholder": "you@example.com"})


class ResetPasswordSetForm(StyledFormMixin, SetPasswordForm):
    pass
