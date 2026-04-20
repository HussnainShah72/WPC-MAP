from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Facility, FacilityContact, FacilityRequirement, FacilityShift, Program, Requirement


REQUIREMENT_TYPE_CHOICES = [
    "Police Check",
    "Hand Hygiene Certificate",
    "Manual Handling Certificate",
    "Flu Vaccination",
    "COVID Vaccination",
    "Immunisation History",
    "NDIS Screening",
    "NDIS Orientation Module",
    "Statutory Declaration",
    "Privacy Confidentiality Form",
    "ID Document",
    "Uniform Policy",
    "Other",
]


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css_class + " form-input").strip()


class FacilityListFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search facilities...", "class": "form-input"}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All statuses"), *Facility.Status.choices],
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    facility_type = forms.ChoiceField(
        required=False,
        label="Type",
        choices=[("", "All types"), *Facility.FacilityType.choices],
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ("name", "Name"),
            ("-name", "Name (Z-A)"),
            ("type", "Type"),
            ("-type", "Type (Z-A)"),
            ("suburb", "Suburb"),
            ("-suburb", "Suburb (Z-A)"),
        ],
        widget=forms.HiddenInput,
    )


class FacilityForm(StyledFormMixin, forms.ModelForm):
    programs = forms.ModelMultipleChoiceField(
        queryset=Program.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Program acceptance",
    )

    class Meta:
        model = Facility
        fields = [
            "name",
            "facility_type",
            "address",
            "postcode",
            "suburb",
            "state",
            "website",
            "phone",
            "quick_notes",
            "status",
            "accepts_students",
            "programs",
            "is_current_students",
            "is_spots_available",
            "is_last_placement",
            "is_next_start",
            "aha_current_students",
            "aha_spots_available",
            "aha_last_placement",
            "aha_next_start",
            "orientation_time",
            "start_time_day1",
            "orientation_required",
            "uniform_policy",
            "parking_info",
            "geo_raw",
            "latitude",
            "longitude",
            "geo_accuracy",
            "geo_verified",
            "mou_complete",
            "contacted_recently",
            "spots",
            "next_start",
        ]
        labels = {
            "name": "Facility name",
            "geo_raw": "Raw coordinates",
            "start_time_day1": "Start time day 1",
            "next_start": "Next start",
            "is_current_students": "IS Current students",
            "is_spots_available": "IS Spots available",
            "is_last_placement": "IS Last placement",
            "is_next_start": "IS Next start",
            "aha_current_students": "AHA Current students",
            "aha_spots_available": "AHA Spots available",
            "aha_last_placement": "AHA Last placement",
            "aha_next_start": "AHA Next start",
        }
        widgets = {
            "address": forms.TextInput(),
            "postcode": forms.TextInput(),
            "state": forms.TextInput(),
            "website": forms.URLInput(),
            "phone": forms.TextInput(),
            "quick_notes": forms.Textarea(attrs={"rows": 4}),
            "uniform_policy": forms.Textarea(attrs={"rows": 3}),
            "parking_info": forms.Textarea(attrs={"rows": 3}),
            "geo_raw": forms.Textarea(attrs={"rows": 3}),
            "orientation_time": forms.TimeInput(attrs={"type": "time"}),
            "start_time_day1": forms.TimeInput(attrs={"type": "time"}),
            "latitude": forms.NumberInput(attrs={"step": "0.000001"}),
            "longitude": forms.NumberInput(attrs={"step": "0.000001"}),
            "next_start": forms.DateInput(attrs={"type": "date"}),
            "spots": forms.NumberInput(attrs={"min": "0"}),
            "is_current_students": forms.NumberInput(attrs={"min": "0"}),
            "is_spots_available": forms.NumberInput(attrs={"min": "0"}),
            "is_last_placement": forms.DateInput(attrs={"type": "date"}),
            "is_next_start": forms.DateInput(attrs={"type": "date"}),
            "aha_current_students": forms.NumberInput(attrs={"min": "0"}),
            "aha_spots_available": forms.NumberInput(attrs={"min": "0"}),
            "aha_last_placement": forms.DateInput(attrs={"type": "date"}),
            "aha_next_start": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["programs"].queryset = Program.objects.filter(name__in=["IS", "AHA"]).order_by("name")
        self.fields["programs"].widget.attrs.pop("class", None)

        placeholders = {
            "name": "Enter facility name",
            "address": "Street address",
            "postcode": "e.g. 6000",
            "suburb": "e.g. Perth",
            "state": "e.g. WA",
            "website": "https://example.com",
            "phone": "(08) 1234 5678",
            "quick_notes": "Add quick notes for placements, logistics, or special instructions",
            "orientation_time": "Select orientation time",
            "start_time_day1": "Select start time",
            "uniform_policy": "Describe dress code or uniform expectations",
            "parking_info": "Add parking instructions or permit details",
            "geo_raw": "Paste map coordinates or geocoding output",
            "latitude": "e.g. -31.9505",
            "longitude": "e.g. 115.8605",
            "spots": "Available spots",
            "next_start": "Choose next start date",
            "is_current_students": "Current IS students",
            "is_spots_available": "Available IS spots",
            "is_last_placement": "Choose last IS placement date",
            "is_next_start": "Choose next IS start date",
            "aha_current_students": "Current AHA students",
            "aha_spots_available": "Available AHA spots",
            "aha_last_placement": "Choose last AHA placement date",
            "aha_next_start": "Choose next AHA start date",
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.setdefault("placeholder", placeholder)

        self.fields["facility_type"].choices = [("", "Select facility type"), *Facility.FacilityType.choices]
        self.fields["status"].choices = [("", "Select status"), *Facility.Status.choices]
        self.fields["geo_accuracy"].choices = [("", "Select accuracy"), *self.fields["geo_accuracy"].choices]
        self.fields["spots"].required = False

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if (latitude and longitude is None) or (longitude and latitude is None):
            error = "Latitude and longitude must both be provided together."
            self.add_error("latitude", error)
            self.add_error("longitude", error)

        if cleaned_data.get("spots") in (None, ""):
            cleaned_data["spots"] = 0

        selected_program_names = {
            program.name.upper()
            for program in cleaned_data.get("programs") or []
            if program and program.name
        }

        if "IS" not in selected_program_names:
            cleaned_data["is_current_students"] = None
            cleaned_data["is_spots_available"] = None
            cleaned_data["is_last_placement"] = None
            cleaned_data["is_next_start"] = None

        if "AHA" not in selected_program_names:
            cleaned_data["aha_current_students"] = None
            cleaned_data["aha_spots_available"] = None
            cleaned_data["aha_last_placement"] = None
            cleaned_data["aha_next_start"] = None

        return cleaned_data


class FacilityShiftForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = FacilityShift
        fields = ["role", "program", "days", "time_range", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].widget.attrs.setdefault("placeholder", "e.g. RN, EN, support worker")
        self.fields["days"].widget.attrs.setdefault("placeholder", "e.g. Mon-Fri")
        self.fields["time_range"].widget.attrs.setdefault("placeholder", "e.g. 7:00 AM - 3:00 PM")
        self.fields["notes"].widget.attrs.setdefault("placeholder", "Shift notes or scheduling context")
        self.fields["program"].choices = [("", "Select program"), *self.fields["program"].choices]


class FacilityRequirementForm(StyledFormMixin, forms.ModelForm):
    requirement_name = forms.ChoiceField(label="Type", required=False, choices=[])
    programs = forms.ModelMultipleChoiceField(
        queryset=Program.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Programs this requirement applies to",
    )

    class Meta:
        model = FacilityRequirement
        fields = ["requirement_name", "mandatory", "programs", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [("", "Select requirement type"), *((item, item) for item in REQUIREMENT_TYPE_CHOICES)]
        current_name = self.instance.requirement.name if self.instance.pk and self.instance.requirement_id else ""
        if current_name and current_name not in REQUIREMENT_TYPE_CHOICES:
            choices.append((current_name, current_name))
        self.fields["requirement_name"].choices = choices
        self.fields["programs"].queryset = Program.objects.filter(name__in=["IS", "AHA"]).order_by("name")
        self.fields["programs"].widget.attrs.pop("class", None)
        self.fields["notes"].widget.attrs.setdefault("placeholder", "Optional notes about this requirement")

        if self.instance.pk and self.instance.requirement_id:
            self.fields["requirement_name"].initial = self.instance.requirement.name
            existing_programs = list(self.instance.programs.all())
            if existing_programs:
                self.fields["programs"].initial = existing_programs
            elif self.instance.program_id:
                self.fields["programs"].initial = [self.instance.program]
        elif not self.is_bound:
            self.fields["mandatory"].initial = False

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get("DELETE"):
            return cleaned_data

        requirement_name = (cleaned_data.get("requirement_name") or "").strip()
        selected_programs = cleaned_data.get("programs") or []
        if self.has_changed() and not requirement_name:
            self.add_error("requirement_name", "Requirement type is required.")
        if self.has_changed() and not selected_programs:
            self.add_error("programs", "Select at least one program.")
        return cleaned_data

    def save(self, commit=True):
        requirement_name = (self.cleaned_data.get("requirement_name") or "").strip()
        if requirement_name:
            self.instance.requirement, _ = Requirement.objects.get_or_create(name=requirement_name)

        selected_programs = list(self.cleaned_data.get("programs") or [])
        self.instance.program = selected_programs[0] if len(selected_programs) == 1 else None
        return super().save(commit=commit)


class FacilityContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = FacilityContact
        fields = ["role", "name", "email", "phone", "programs"]
        widgets = {
            "programs": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].widget.attrs.setdefault("placeholder", "e.g. Placement coordinator")
        self.fields["name"].widget.attrs.setdefault("placeholder", "Contact full name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "(08) 1234 5678")
        self.fields["programs"].queryset = Program.objects.filter(name__in=["IS", "AHA"]).order_by("name")
        self.fields["programs"].widget.attrs.pop("class", None)


class RequiredInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        if "DELETE" in form.fields:
            form.fields["DELETE"].widget.attrs["class"] = "form-checkbox"


class FacilityRequirementInlineFormSet(RequiredInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or form.cleaned_data.get("DELETE"):
                continue
            requirement_name = (form.cleaned_data.get("requirement_name") or "").strip().lower()
            if not requirement_name:
                continue
            selected_programs = tuple(sorted(program.pk for program in form.cleaned_data.get("programs") or []))
            key = (requirement_name, selected_programs)
            if key in seen:
                raise forms.ValidationError("Duplicate requirements for the same program selection are not allowed.")
            seen.add(key)


FacilityShiftFormSet = inlineformset_factory(
    Facility,
    FacilityShift,
    form=FacilityShiftForm,
    formset=RequiredInlineFormSet,
    extra=1,
    can_delete=True,
)

FacilityRequirementFormSet = inlineformset_factory(
    Facility,
    FacilityRequirement,
    form=FacilityRequirementForm,
    formset=FacilityRequirementInlineFormSet,
    extra=1,
    can_delete=True,
)

FacilityContactFormSet = inlineformset_factory(
    Facility,
    FacilityContact,
    form=FacilityContactForm,
    formset=RequiredInlineFormSet,
    extra=1,
    can_delete=True,
)
