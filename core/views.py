import math

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts.models import AllowedSignupEmail, User
from accounts.permissions import AdminRequiredMixin, ViewerRequiredMixin
from facilities.models import Facility

from .forms import AddUserAccessForm, EditUserAccessForm, MapFilterForm
from .wa_suburbs import WA_SUBURBS, WA_SUBURB_COORDINATES


class HomeView(ViewerRequiredMixin, TemplateView):
    template_name = "core/home.html"

    def get_filter_form(self):
        return MapFilterForm(self.request.GET or None)

    def normalize_suburb(self, suburb):
        return " ".join((suburb or "").split()).strip().lower()

    def haversine_km(self, lat1, lon1, lat2, lon2):
        radius = 6371.0
        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        delta_phi = math.radians(float(lat2) - float(lat1))
        delta_lambda = math.radians(float(lon2) - float(lon1))
        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

    def get_suburb_center(self, suburb):
        normalized = self.normalize_suburb(suburb)
        if not normalized:
            return None

        for suburb_name, coordinates in WA_SUBURB_COORDINATES.items():
            if self.normalize_suburb(suburb_name) == normalized:
                return {
                    "name": suburb_name,
                    "latitude": float(coordinates["latitude"]),
                    "longitude": float(coordinates["longitude"]),
                    "source": "dataset",
                }

        suburb_matches = list(
            Facility.objects.filter(
                suburb__iexact=suburb,
                latitude__isnull=False,
                longitude__isnull=False,
            )
        )
        if not suburb_matches:
            return None

        center_lat = sum(float(facility.latitude) for facility in suburb_matches) / len(suburb_matches)
        center_lon = sum(float(facility.longitude) for facility in suburb_matches) / len(suburb_matches)
        return {
            "name": suburb_matches[0].suburb,
            "latitude": center_lat,
            "longitude": center_lon,
            "source": "facilities",
        }

    def apply_radius(self, facilities, suburb, radius_km):
        if not suburb or not radius_km:
            return facilities, None, None

        suburb_center = self.get_suburb_center(suburb)
        if not suburb_center:
            return facilities, "Radius filtering is only applied when the selected suburb has known coordinates or mapped facilities.", None

        filtered = []
        for facility in facilities:
            if facility.latitude is None or facility.longitude is None:
                continue
            distance = self.haversine_km(
                suburb_center["latitude"],
                suburb_center["longitude"],
                facility.latitude,
                facility.longitude,
            )
            if distance <= radius_km:
                filtered.append(facility)

        return filtered, None, {
            "suburb_name": suburb_center["name"],
            "radius_km": radius_km,
            "center": {
                "latitude": suburb_center["latitude"],
                "longitude": suburb_center["longitude"],
            },
            "source": suburb_center["source"],
        }

    def get_facilities(self):
        form = self.get_filter_form()
        queryset = Facility.objects.prefetch_related("programs").filter(latitude__isnull=False, longitude__isnull=False)

        if not form.is_valid():
            return list(queryset.order_by("name")), None, None

        keyword = form.cleaned_data.get("q")
        suburb = form.cleaned_data.get("suburb")
        radius = form.cleaned_data.get("radius")
        facility_type = form.cleaned_data.get("facility_type")
        status = form.cleaned_data.get("status")

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(address__icontains=keyword)
                | Q(suburb__icontains=keyword)
                | Q(postcode__icontains=keyword)
                | Q(phone__icontains=keyword)
                | Q(website__icontains=keyword)
                | Q(quick_notes__icontains=keyword)
            )
        if facility_type:
            queryset = queryset.filter(facility_type=facility_type)
        if status:
            queryset = queryset.filter(status=status)

        facilities = list(queryset.order_by("name"))
        radius_note = None
        map_filter_state = None

        if suburb and radius:
            facilities, radius_note, map_filter_state = self.apply_radius(facilities, suburb, int(radius))
        elif suburb:
            facilities = [facility for facility in facilities if facility.suburb and suburb.lower() in facility.suburb.lower()]

        return facilities, radius_note, map_filter_state

    def serialize_facility(self, facility):
        return {
            "id": facility.pk,
            "name": facility.name,
            "type": facility.get_facility_type_display(),
            "type_key": facility.facility_type,
            "status": facility.get_status_display(),
            "status_key": facility.status,
            "address": ", ".join(part for part in [facility.address, facility.suburb, facility.state, facility.postcode] if part) or "-",
            "phone": facility.phone or "-",
            "website": facility.website or "",
            "notes": facility.quick_notes or "No quick notes yet.",
            "latitude": float(facility.latitude),
            "longitude": float(facility.longitude),
            "programs": [program.name for program in facility.programs.all()],
            "edit_url": reverse_lazy("facilities:edit", kwargs={"pk": facility.pk}),
            "delete_url": reverse_lazy("facilities:delete", kwargs={"pk": facility.pk}),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_filter_form()
        facilities, radius_note, map_filter_state = self.get_facilities()
        serialized = [self.serialize_facility(facility) for facility in facilities]
        selected_suburb = ""
        selected_radius = ""
        if form.is_valid():
            selected_suburb = form.cleaned_data.get("suburb") or ""
            selected_radius = form.cleaned_data.get("radius") or ""

        radius_summary = None
        if map_filter_state:
            radius_summary = f"Within {map_filter_state['radius_km']} km of {map_filter_state['suburb_name']}"

        context.update(
            {
                "filter_form": form,
                "facilities": facilities,
                "facility_results": serialized,
                "facility_results_json": serialized,
                "results_count": len(serialized),
                "results_summary": f"Showing {len(serialized)} results",
                "radius_summary": radius_summary,
                "sort_indicator": "Sorted A-Z",
                "reset_url": reverse_lazy("core:home"),
                "radius_note": radius_note,
                "wa_suburbs": WA_SUBURBS,
                "map_filter_state": {
                    "selected_suburb": selected_suburb,
                    "radius_km": int(selected_radius) if selected_radius else None,
                    "suburb_center": map_filter_state["center"] if map_filter_state else None,
                },
            }
        )
        return context


class AdminDashboardView(AdminRequiredMixin, FormView):
    template_name = "core/admin_dashboard.html"
    form_class = AddUserAccessForm
    success_url = reverse_lazy("core_admin:dashboard")

    def form_valid(self, form):
        access_record = form.save()
        messages.success(self.request, f"Access saved for {access_record.email}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = list(User.objects.all().order_by("email"))
        users_by_email = {user.email.lower(): user for user in users}
        access_records_by_email = {
            record.email.lower(): record
            for record in AllowedSignupEmail.objects.order_by("-created_at", "email")
        }

        for user in users:
            user_email = user.email.lower()
            access_record = access_records_by_email.get(user_email)
            if access_record is None:
                access_record = AllowedSignupEmail.objects.create(
                    email=user.email,
                    role=user.role,
                    is_registered=True,
                )
                access_records_by_email[user_email] = access_record
                continue

            update_fields = []
            if access_record.role != user.role:
                access_record.role = user.role
                update_fields.append("role")
            if not access_record.is_registered:
                access_record.is_registered = True
                update_fields.append("is_registered")
            if update_fields:
                access_record.save(update_fields=update_fields)

        access_records = sorted(
            access_records_by_email.values(),
            key=lambda record: (record.created_at, record.email.lower()),
            reverse=True,
        )
        entries = []
        for record in access_records:
            user = users_by_email.get(record.email.lower())
            entries.append(
                {
                    "record": record,
                    "user": user,
                    "is_registered": bool(user) or record.is_registered,
                }
            )
        context.update(
            {
                "subtitle": "Manage users and system access permissions",
                "total_user_count": len(entries),
                "access_entries": entries,
            }
        )
        return context


class AdminAccessEditView(AdminRequiredMixin, FormView):
    template_name = "core/admin_user_form.html"
    form_class = EditUserAccessForm
    success_url = reverse_lazy("core_admin:dashboard")

    def dispatch(self, request, *args, **kwargs):
        self.access_record = get_object_or_404(AllowedSignupEmail, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.access_record
        return kwargs

    def form_valid(self, form):
        if self.access_record.email.lower() == self.request.user.email.lower() and form.cleaned_data["role"] != User.Roles.ADMIN:
            form.add_error("role", "You cannot remove your own admin role.")
            return self.form_invalid(form)

        access_record = form.save()
        messages.success(self.request, f"Updated access for {access_record.email}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "Edit User Access",
                "subtitle": "Update the invited user's role and access level",
                "submit_label": "Save Changes",
                "cancel_url": reverse_lazy("core_admin:dashboard"),
                "access_record": self.access_record,
            }
        )
        return context


class AdminAccessDeleteView(AdminRequiredMixin, TemplateView):
    template_name = "core/admin_user_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        self.access_record = get_object_or_404(AllowedSignupEmail, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = self.access_record.email
        linked_user = User.objects.filter(email__iexact=email).first()
        if linked_user and linked_user.pk == request.user.pk:
            messages.error(request, "You cannot remove your own admin access.")
            return redirect("core_admin:dashboard")

        if linked_user:
            linked_user.delete()
        self.access_record.delete()
        messages.success(request, f"Access removed for {email}.")
        return redirect("core_admin:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        linked_user = User.objects.filter(email__iexact=self.access_record.email).first()
        context.update(
            {
                "page_title": "Delete User Access",
                "subtitle": "Remove this invitation or user access record safely",
                "access_record": self.access_record,
                "linked_user": linked_user,
                "cancel_url": reverse_lazy("core_admin:dashboard"),
            }
        )
        return context
