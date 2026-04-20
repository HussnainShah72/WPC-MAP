from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "program"
        verbose_name_plural = "programs"

    def __str__(self) -> str:
        return self.name


class Requirement(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "requirement"
        verbose_name_plural = "requirements"

    def __str__(self) -> str:
        return self.name


class Facility(models.Model):
    class FacilityType(models.TextChoices):
        AGED_CARE = "aged_care", "Aged Care"
        ALLIED_HEALTH = "allied_health", "Allied Health"
        HOSPITAL = "hospital", "Hospital"
        CLINIC = "clinic", "Clinic"
        REHABILITATION = "rehabilitation", "Rehabilitation"
        PHARMACY = "pharmacy", "Pharmacy"
        PHYSIOTHERAPY = "physiotherapy", "Physiotherapy"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        ACTIVE = "active_placements", "Active placements"
        UPCOMING = "upcoming_placements", "Upcoming placements"
        PREVIOUS = "previous_placements", "Previous placements"
        POTENTIAL = "potential", "Potential"
        NOT_AVAILABLE = "not_available", "Not available"

    class GeoAccuracy(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        APPROXIMATE = "approximate", "Approximate"
        EXACT = "exact", "Exact"

    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=30, choices=FacilityType.choices)
    address = models.CharField(max_length=255, blank=True)
    suburb = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    quick_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.POTENTIAL,
    )
    accepts_students = models.BooleanField(default=False)
    is_current_students = models.PositiveIntegerField(blank=True, null=True)
    is_spots_available = models.PositiveIntegerField(blank=True, null=True)
    is_last_placement = models.DateField(blank=True, null=True)
    is_next_start = models.DateField(blank=True, null=True)
    aha_current_students = models.PositiveIntegerField(blank=True, null=True)
    aha_spots_available = models.PositiveIntegerField(blank=True, null=True)
    aha_last_placement = models.DateField(blank=True, null=True)
    aha_next_start = models.DateField(blank=True, null=True)
    orientation_required = models.BooleanField(default=False)
    uniform_policy = models.TextField(blank=True)
    parking_info = models.TextField(blank=True)
    orientation_time = models.TimeField(blank=True, null=True)
    start_time_day1 = models.TimeField(blank=True, null=True)
    mou_complete = models.BooleanField(default=False)
    contacted_recently = models.BooleanField(default=False)
    spots = models.PositiveIntegerField(default=0)
    next_start = models.DateField(blank=True, null=True)
    geo_raw = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    geo_accuracy = models.CharField(
        max_length=20,
        choices=GeoAccuracy.choices,
        default=GeoAccuracy.UNKNOWN,
    )
    geo_verified = models.BooleanField(default=False)
    programs = models.ManyToManyField(
        Program,
        blank=True,
        related_name="facilities",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "facility"
        verbose_name_plural = "facilities"

    def __str__(self) -> str:
        return self.name


class FacilityRequirement(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="facility_requirements",
    )
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        related_name="facility_requirements",
    )
    mandatory = models.BooleanField(default=True)
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="facility_requirements",
    )
    programs = models.ManyToManyField(
        Program,
        blank=True,
        related_name="facility_requirement_items",
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["facility__name", "requirement__name"]
        verbose_name = "facility requirement"
        verbose_name_plural = "facility requirements"
        unique_together = ("facility", "requirement", "program")

    def __str__(self) -> str:
        if self.pk:
            selected_programs = list(self.programs.order_by("name").values_list("name", flat=True))
            if selected_programs:
                return f"{self.facility} - {self.requirement} ({', '.join(selected_programs)})"
        if self.program:
            return f"{self.facility} - {self.requirement} ({self.program})"
        return f"{self.facility} - {self.requirement}"


class FacilityShift(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="shifts",
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="facility_shifts",
    )
    role = models.CharField(max_length=120, blank=True)
    days = models.CharField(max_length=255)
    time_range = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["facility__name", "days", "time_range"]
        verbose_name = "facility shift"
        verbose_name_plural = "facility shifts"

    def __str__(self) -> str:
        program_name = self.program.name if self.program else "General"
        return f"{self.facility} - {program_name} - {self.days}"


class FacilityContact(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    role = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    programs = models.ManyToManyField(
        Program,
        blank=True,
        related_name="facility_contacts",
    )

    class Meta:
        ordering = ["facility__name", "name"]
        verbose_name = "facility contact"
        verbose_name_plural = "facility contacts"

    def __str__(self) -> str:
        return f"{self.name} ({self.facility})"
