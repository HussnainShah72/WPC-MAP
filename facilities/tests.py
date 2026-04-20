from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from facilities.models import Facility, Program


class FacilityFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.viewer = User.objects.create_user(
            email="viewer@example.com",
            password="ViewerPass123!",
            role=User.Roles.VIEWER,
        )
        cls.coordinator = User.objects.create_user(
            email="coordinator@example.com",
            password="CoordinatorPass123!",
            role=User.Roles.COORDINATOR,
        )
        cls.admin = User.objects.create_user(
            email="admin@example.com",
            password="AdminPass123!",
            role=User.Roles.ADMIN,
        )
        cls.program_is = Program.objects.create(name="IS")
        cls.program_aha = Program.objects.create(name="AHA")
        cls.facility = Facility.objects.create(
            name="Alpha Clinic",
            facility_type=Facility.FacilityType.CLINIC,
            suburb="Perth",
            address="1 Alpha Street",
            status=Facility.Status.ACTIVE,
            spots=2,
            latitude=Decimal("-31.950500"),
            longitude=Decimal("115.860500"),
        )
        cls.facility.programs.add(cls.program_is)
        cls.other_facility = Facility.objects.create(
            name="Bravo Hospital",
            facility_type=Facility.FacilityType.HOSPITAL,
            suburb="Fremantle",
            address="2 Bravo Street",
            status=Facility.Status.NOT_AVAILABLE,
            spots=4,
            latitude=Decimal("-32.056900"),
            longitude=Decimal("115.743900"),
        )
        cls.other_facility.programs.add(cls.program_aha)

    def facility_form_payload(self, **overrides):
        data = {
            "name": "Created Facility",
            "facility_type": Facility.FacilityType.AGED_CARE,
            "address": "100 New Street",
            "postcode": "6000",
            "suburb": "Perth",
            "state": "WA",
            "website": "https://example.com",
            "phone": "0899999999",
            "quick_notes": "Useful notes",
            "status": Facility.Status.UPCOMING,
            "accepts_students": "on",
            "programs": [str(self.program_is.pk)],
            "orientation_time": "08:30",
            "start_time_day1": "09:00",
            "orientation_required": "on",
            "uniform_policy": "Closed shoes",
            "parking_info": "Street parking",
            "geo_raw": "-31.95,115.86",
            "latitude": "-31.950500",
            "longitude": "115.860500",
            "geo_accuracy": Facility.GeoAccuracy.EXACT,
            "geo_verified": "on",
            "mou_complete": "on",
            "contacted_recently": "on",
            "spots": "3",
            "next_start": "2026-04-01",
            "shifts-TOTAL_FORMS": "1",
            "shifts-INITIAL_FORMS": "0",
            "shifts-MIN_NUM_FORMS": "0",
            "shifts-MAX_NUM_FORMS": "1000",
            "shifts-0-role": "Morning",
            "shifts-0-program": str(self.program_is.pk),
            "shifts-0-days": "Mon-Fri",
            "shifts-0-time_range": "08:00-16:00",
            "shifts-0-notes": "Primary shift",
            "requirements-TOTAL_FORMS": "1",
            "requirements-INITIAL_FORMS": "0",
            "requirements-MIN_NUM_FORMS": "0",
            "requirements-MAX_NUM_FORMS": "1000",
            "requirements-0-requirement_name": "Police Check",
            "requirements-0-mandatory": "on",
            "requirements-0-programs": [str(self.program_is.pk)],
            "requirements-0-notes": "Bring original certificate",
            "contacts-TOTAL_FORMS": "1",
            "contacts-INITIAL_FORMS": "0",
            "contacts-MIN_NUM_FORMS": "0",
            "contacts-MAX_NUM_FORMS": "1000",
            "contacts-0-role": "Coordinator",
            "contacts-0-name": "Jamie Smith",
            "contacts-0-email": "jamie@example.com",
            "contacts-0-phone": "0800000000",
            "contacts-0-programs": [str(self.program_is.pk)],
        }
        data.update(overrides)
        return data

    def test_coordinator_can_create_facility(self):
        self.client.force_login(self.coordinator)

        response = self.client.post(reverse("facilities:create"), self.facility_form_payload())

        self.assertRedirects(response, reverse("facilities:list"))
        created = Facility.objects.get(name="Created Facility")
        self.assertEqual(created.status, Facility.Status.UPCOMING)
        self.assertEqual(created.spots, 3)
        self.assertTrue(created.shifts.exists())
        self.assertTrue(created.contacts.exists())
        self.assertTrue(created.facility_requirements.exists())
        self.assertTrue(created.facility_requirements.first().programs.filter(pk=self.program_is.pk).exists())

    def test_coordinator_can_edit_facility(self):
        self.client.force_login(self.coordinator)

        response = self.client.post(
            reverse("facilities:edit", kwargs={"pk": self.facility.pk}),
            self.facility_form_payload(name="Updated Alpha Clinic", facility_type=Facility.FacilityType.CLINIC),
        )

        self.assertRedirects(response, reverse("facilities:list"))
        self.facility.refresh_from_db()
        self.assertEqual(self.facility.name, "Updated Alpha Clinic")

    def test_viewer_cannot_access_create_facility(self):
        self.client.force_login(self.viewer)

        response = self.client.get(reverse("facilities:create"))

        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_facility(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse("facilities:delete", kwargs={"pk": self.other_facility.pk}))

        self.assertRedirects(response, reverse("facilities:list"))
        self.assertFalse(Facility.objects.filter(pk=self.other_facility.pk).exists())

    def test_facilities_list_filters(self):
        self.client.force_login(self.viewer)

        response = self.client.get(
            reverse("facilities:list"),
            {"q": "Alpha", "status": Facility.Status.ACTIVE, "facility_type": Facility.FacilityType.CLINIC},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Clinic")
        self.assertNotContains(response, "Bravo Hospital")

    def test_detail_fragments_endpoint_returns_panel_and_modal(self):
        self.client.force_login(self.viewer)

        response = self.client.get(reverse("facilities:detail_fragments", kwargs={"pk": self.facility.pk}))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("panel_html", payload)
        self.assertIn("modal_html", payload)
        self.assertIn("Alpha Clinic", payload["panel_html"])
        self.assertIn("Overview", payload["modal_html"])
