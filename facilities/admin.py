from django.contrib import admin

from .models import Facility, FacilityContact, FacilityRequirement, FacilityShift, Program, Requirement


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class FacilityRequirementInline(admin.TabularInline):
    model = FacilityRequirement
    extra = 0


class FacilityShiftInline(admin.TabularInline):
    model = FacilityShift
    extra = 0


class FacilityContactInline(admin.TabularInline):
    model = FacilityContact
    extra = 0


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "facility_type", "status", "suburb", "spots", "next_start")
    list_filter = ("facility_type", "status", "accepts_students", "geo_verified")
    search_fields = ("name", "suburb", "address", "postcode")
    filter_horizontal = ("programs",)
    inlines = (FacilityRequirementInline, FacilityShiftInline, FacilityContactInline)


@admin.register(FacilityRequirement)
class FacilityRequirementAdmin(admin.ModelAdmin):
    list_display = ("facility", "requirement", "display_programs", "mandatory")
    list_filter = ("mandatory", "programs")
    search_fields = ("facility__name", "requirement__name", "notes")
    filter_horizontal = ("programs",)

    def display_programs(self, obj):
        program_names = list(obj.programs.order_by("name").values_list("name", flat=True))
        if program_names:
            return ", ".join(program_names)
        if obj.program:
            return obj.program.name
        return "-"

    display_programs.short_description = "Programs"


@admin.register(FacilityShift)
class FacilityShiftAdmin(admin.ModelAdmin):
    list_display = ("facility", "program", "days", "time_range")
    list_filter = ("program",)
    search_fields = ("facility__name", "days", "time_range", "notes")


@admin.register(FacilityContact)
class FacilityContactAdmin(admin.ModelAdmin):
    list_display = ("name", "facility", "role", "email", "phone")
    list_filter = ("programs",)
    search_fields = ("name", "facility__name", "role", "email", "phone")
