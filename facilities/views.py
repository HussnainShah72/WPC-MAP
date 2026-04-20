from pprint import pformat

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch, Q
from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View

from accounts.permissions import AdminRequiredMixin, CoordinatorRequiredMixin, ViewerRequiredMixin

from .forms import (
    FacilityContactFormSet,
    FacilityForm,
    FacilityListFilterForm,
    FacilityRequirementFormSet,
    FacilityShiftFormSet,
)
from .models import Facility, FacilityContact, FacilityRequirement, FacilityShift, Program


class FacilityDetailContextMixin:
    def get_detail_queryset(self):
        return Facility.objects.prefetch_related(
            "programs",
            Prefetch(
                "facility_requirements",
                queryset=FacilityRequirement.objects.select_related("requirement", "program").prefetch_related("programs").order_by("requirement__name"),
            ),
            Prefetch("shifts", queryset=FacilityShift.objects.select_related("program").order_by("days", "time_range")),
            Prefetch("contacts", queryset=FacilityContact.objects.prefetch_related("programs").order_by("name")),
        )

    def get_facility_with_details(self, pk):
        return get_object_or_404(self.get_detail_queryset(), pk=pk)

    def build_detail_context(self, facility):
        primary_contact = facility.contacts.first()
        website_href = facility.website or ""
        phone_href = "tel:" + facility.phone.replace(" ", "") if facility.phone else ""
        email_href = f"mailto:{primary_contact.email}" if primary_contact and primary_contact.email else ""
        address_parts = [facility.address, facility.suburb, facility.state, facility.postcode]
        address_text = ", ".join(part for part in address_parts if part) or "-"
        directions_href = "https://www.google.com/maps/search/?api=1&query=" + address_text.replace(" ", "+") if address_text != "-" else ""
        return {
            "facility": facility,
            "primary_contact": primary_contact,
            "website_href": website_href,
            "phone_href": phone_href,
            "email_href": email_href,
            "directions_href": directions_href,
            "address_text": address_text,
        }


class FacilityListView(ViewerRequiredMixin, FacilityDetailContextMixin, TemplateView):
    template_name = "facilities/list.html"

    sort_map = {
        "name": "name",
        "-name": "-name",
        "type": "facility_type",
        "-type": "-facility_type",
        "suburb": "suburb",
        "-suburb": "-suburb",
    }

    def get_filter_form(self):
        return FacilityListFilterForm(self.request.GET or None)

    def get_queryset(self):
        form = self.get_filter_form()
        queryset = Facility.objects.prefetch_related("programs").all()

        if form.is_valid():
            keyword = form.cleaned_data.get("q")
            status = form.cleaned_data.get("status")
            facility_type = form.cleaned_data.get("facility_type")
            sort = form.cleaned_data.get("sort") or "name"

            if keyword:
                queryset = queryset.filter(
                    Q(name__icontains=keyword)
                    | Q(suburb__icontains=keyword)
                    | Q(address__icontains=keyword)
                    | Q(postcode__icontains=keyword)
                    | Q(phone__icontains=keyword)
                    | Q(quick_notes__icontains=keyword)
                )
            if status:
                queryset = queryset.filter(status=status)
            if facility_type:
                queryset = queryset.filter(facility_type=facility_type)

            queryset = queryset.order_by(self.sort_map.get(sort, "name"))
        else:
            queryset = queryset.order_by("name")

        return queryset

    def build_sort_url(self, sort_value):
        params = QueryDict(mutable=True)
        for key, value in self.request.GET.items():
            if value:
                params[key] = value
        params["sort"] = sort_value
        query_string = params.urlencode()
        return f"?{query_string}" if query_string else "?sort=name"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_filter_form()
        facilities = list(self.get_queryset())
        current_sort = self.request.GET.get("sort") or "name"

        context.update(
            {
                "filter_form": form,
                "facilities": facilities,
                "sort_urls": {
                    "name": self.build_sort_url("-name" if current_sort == "name" else "name"),
                    "type": self.build_sort_url("-type" if current_sort == "type" else "type"),
                    "suburb": self.build_sort_url("-suburb" if current_sort == "suburb" else "suburb"),
                },
                "current_sort": current_sort,
                "facility_count": len(facilities),
            }
        )
        return context


class FacilityDetailView(ViewerRequiredMixin, FacilityDetailContextMixin, TemplateView):
    template_name = "facilities/detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.facility = self.get_facility_with_details(kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.build_detail_context(self.facility))
        return context


class FacilityFormView(CoordinatorRequiredMixin, TemplateView):
    template_name = "facilities/form.html"
    facility = None

    def debug_validation_errors(self, form, formsets):
        if not settings.DEBUG:
            return

        debug_payload = {
            "form_errors": form.errors,
            "form_non_field_errors": form.non_field_errors(),
            "shift_formset_errors": formsets["shift_formset"].errors,
            "shift_formset_non_form_errors": formsets["shift_formset"].non_form_errors(),
            "shift_management_form_errors": formsets["shift_formset"].management_form.errors,
            "requirement_formset_errors": formsets["requirement_formset"].errors,
            "requirement_formset_non_form_errors": formsets["requirement_formset"].non_form_errors(),
            "requirement_management_form_errors": formsets["requirement_formset"].management_form.errors,
            "contact_formset_errors": formsets["contact_formset"].errors,
            "contact_formset_non_form_errors": formsets["contact_formset"].non_form_errors(),
            "contact_management_form_errors": formsets["contact_formset"].management_form.errors,
        }
        print("FACILITY FORM DEBUG ERRORS\n" + pformat(debug_payload))

    def dispatch(self, request, *args, **kwargs):
        self.ensure_base_programs()
        self.facility = self.get_facility()
        return super().dispatch(request, *args, **kwargs)

    def ensure_base_programs(self):
        for program_name in ["IS", "AHA"]:
            Program.objects.get_or_create(name=program_name)

    def get_facility(self):
        return Facility()

    def get_form(self, data=None):
        return FacilityForm(data=data, instance=self.facility)

    def get_formsets(self, data=None):
        return {
            "shift_formset": FacilityShiftFormSet(data=data, instance=self.facility, prefix="shifts"),
            "requirement_formset": FacilityRequirementFormSet(data=data, instance=self.facility, prefix="requirements"),
            "contact_formset": FacilityContactFormSet(data=data, instance=self.facility, prefix="contacts"),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = kwargs.get("form") or self.get_form()
        formsets = kwargs.get("formsets") or self.get_formsets()
        is_edit = bool(self.facility and self.facility.pk)
        context.update(
            {
                "form": form,
                "shift_formset": formsets["shift_formset"],
                "requirement_formset": formsets["requirement_formset"],
                "contact_formset": formsets["contact_formset"],
                "is_edit": is_edit,
                "page_title": "Edit Facility" if is_edit else "Add Facility",
                "page_subtitle": "Update facility placement, compliance, geo, and contact information."
                if is_edit
                else "Create a new placement facility record with schedule, compliance, and contact details.",
                "cancel_url": reverse_lazy("facilities:list"),
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        is_edit = bool(self.facility and self.facility.pk)
        form = self.get_form(data=request.POST)
        formsets = self.get_formsets(data=request.POST)

        if form.is_valid() and all(formset.is_valid() for formset in formsets.values()):
            self.save_all(form, formsets)
            messages.success(
                request,
                f"Facility {'updated' if is_edit else 'created'} successfully.",
            )
            return redirect("facilities:list")

        self.debug_validation_errors(form, formsets)
        messages.error(request, "Please correct the errors below and try again.")
        return self.render_to_response(self.get_context_data(form=form, formsets=formsets))

    @transaction.atomic
    def save_all(self, form, formsets):
        facility = form.save()
        self.save_formset(formsets["shift_formset"], facility)
        self.save_formset(formsets["requirement_formset"], facility)
        self.save_formset(formsets["contact_formset"], facility)

    def save_formset(self, formset, facility):
        instances = formset.save(commit=False)
        for deleted_obj in formset.deleted_objects:
            deleted_obj.delete()
        for instance in instances:
            instance.facility = facility
            instance.save()
        formset.save_m2m()


class FacilityCreateView(FacilityFormView):
    pass


class FacilityUpdateView(FacilityFormView):
    def get_facility(self):
        return get_object_or_404(Facility, pk=self.kwargs["pk"])


class FacilityDeleteView(AdminRequiredMixin, TemplateView):
    template_name = "facilities/delete_confirm.html"

    def dispatch(self, request, *args, **kwargs):
        self.facility = get_object_or_404(Facility, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        facility_name = self.facility.name
        self.facility.delete()
        messages.success(request, f"Facility '{facility_name}' deleted successfully.")
        return redirect("facilities:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "facility": self.facility,
                "cancel_url": reverse_lazy("facilities:list"),
            }
        )
        return context


class FacilityDetailFragmentsView(ViewerRequiredMixin, FacilityDetailContextMixin, View):
    def get(self, request, *args, **kwargs):
        facility = self.get_facility_with_details(kwargs["pk"])
        context = self.build_detail_context(facility)
        panel_html = render_to_string("facilities/partials/facility_detail_panel.html", context, request=request)
        modal_html = render_to_string("facilities/partials/facility_detail_modal.html", context, request=request)
        return JsonResponse({
            "panel_html": panel_html,
            "modal_html": modal_html,
        })
