from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class AuthFlowTests(TestCase):
    def test_insight_signup_creates_admin_user(self):
        response = self.client.post(
            reverse("accounts:sign_up"),
            {
                "email": "approved@insight.edu.au",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("core:home"))
        user = User.objects.get(email="approved@insight.edu.au")
        self.assertEqual(user.role, User.Roles.ADMIN)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_non_insight_signup_creates_viewer_user(self):
        response = self.client.post(
            reverse("accounts:sign_up"),
            {
                "email": "viewer@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("core:home"))
        user = User.objects.get(email="viewer@example.com")
        self.assertEqual(user.role, User.Roles.VIEWER)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_login_invalid_shows_expected_message(self):
        User.objects.create_user(email="viewer@example.com", password="CorrectPass123!", role=User.Roles.VIEWER)

        response = self.client.post(
            reverse("accounts:login"),
            {
                "email": "viewer@example.com",
                "password": "WrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid login credentials")

    def test_login_success_redirects_home(self):
        User.objects.create_user(email="viewer@example.com", password="CorrectPass123!", role=User.Roles.VIEWER)

        response = self.client.post(
            reverse("accounts:login"),
            {
                "email": "viewer@example.com",
                "password": "CorrectPass123!",
            },
        )

        self.assertRedirects(response, reverse("core:home"))
