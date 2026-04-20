from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import AllowedSignupEmail, User
from facilities.models import Facility, Program


class AdminAndMapTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.viewer = User.objects.create_user(
            email="viewer@example.com",
            password="ViewerPass123!",
            role=User.Roles.VIEWER,
        )
        cls.admin = User.objects.create_user(
            email="admin@example.com",
            password="AdminPass123!",
            role=User.Roles.ADMIN,
        )
        cls.program = Program.objects.create(name="IS")
        cls.facility = Facility.objects.create(
            name="Map Ready Facility",
            facility_type=Facility.FacilityType.CLINIC,
            status=Facility.Status.ACTIVE,
            suburb="Perth",
            address="123 Example Street",
            latitude=Decimal("-31.950500"),
            longitude=Decimal("115.860500"),
        )
        cls.facility.programs.add(cls.program)

    def test_viewer_can_render_map_homepage(self):
        self.client.force_login(self.viewer)

        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "WPC Map")
        self.assertContains(response, "Map Ready Facility")

    def test_admin_can_add_user_access(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("core_admin:dashboard"),
            {"email": "invitee@example.com", "role": User.Roles.COORDINATOR},
        )

        self.assertRedirects(response, reverse("core_admin:dashboard"))
        self.assertTrue(AllowedSignupEmail.objects.filter(email="invitee@example.com", role=User.Roles.COORDINATOR).exists())

    def test_viewer_cannot_access_admin_panel(self):
        self.client.force_login(self.viewer)

        response = self.client.get(reverse("core_admin:dashboard"))

        self.assertEqual(response.status_code, 403)
