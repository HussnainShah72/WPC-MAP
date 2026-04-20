from django import forms

from accounts.models import AllowedSignupEmail, User
from facilities.models import Facility


class StyledAdminFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-input")


class AddUserAccessForm(StyledAdminFormMixin, forms.Form):
    email = forms.EmailField(label="Email Address")
    role = forms.ChoiceField(label="Role", choices=User.Roles.choices)

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def save(self):
        email = self.cleaned_data["email"]
        role = self.cleaned_data["role"]
        allowed_signup, _ = AllowedSignupEmail.objects.update_or_create(
            email=email,
            defaults={"role": role},
        )
        user = User.objects.filter(email__iexact=email).first()
        if user:
            user.role = role
            user.save(update_fields=["role"])
            if not allowed_signup.is_registered:
                allowed_signup.is_registered = True
                allowed_signup.save(update_fields=["is_registered"])
        return allowed_signup


class EditUserAccessForm(StyledAdminFormMixin, forms.ModelForm):
    class Meta:
        model = AllowedSignupEmail
        fields = ["email", "role"]
        labels = {
            "email": "Email Address",
            "role": "Role",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True

    def save(self, commit=True):
        allowed_signup = super().save(commit=commit)
        user = User.objects.filter(email__iexact=allowed_signup.email).first()
        if user and user.role != allowed_signup.role:
            user.role = allowed_signup.role
            user.save(update_fields=["role"])
        return allowed_signup


class MapFilterForm(forms.Form):
    RADIUS_CHOICES = [
        ("", "All distances"),
        ("5", "5 km"),
        ("10", "10 km"),
        ("15", "15 km"),
        ("20", "20 km"),
        ("25", "25 km"),
        ("30", "30 km"),
    ]

    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search by anything...", "class": "form-input"}),
    )
    suburb = forms.CharField(
        required=False,
        label="Suburb",
        widget=forms.TextInput(attrs={"placeholder": "Search by suburb...", "class": "form-input", "autocomplete": "off", "spellcheck": "false", "data-suburb-input": "true"}),
    )
    radius = forms.ChoiceField(
        required=False,
        choices=RADIUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    facility_type = forms.ChoiceField(
        required=False,
        label="Type",
        choices=[("", "All types"), *Facility.FacilityType.choices],
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    status = forms.ChoiceField(
        required=False,
        label="Status",
        choices=[("", "All statuses"), *Facility.Status.choices],
        widget=forms.Select(attrs={"class": "form-input"}),
    )


