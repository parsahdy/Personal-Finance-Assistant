from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User


class RegisterViewTest(APITestCase):

    def test_register_user(self):

        url = reverse("register")

        data = {
            "first_name": "Bizhan",
            "last_name": "Mozi",
            "username": "Bizhoorkhan",
            "email": "Bizhoorkhan@gmail.com",
            "password": "Bizh1234",
            "confirm_password": "Bizh1234",
            "country": "Iran"
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "Bizhoorkhan")


class LoginTestView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

    def test_login_success(self):

        url = reverse("login")

        data = {
            "username": "Bizhoorkhan",
            "password": "Bizh1234"
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class ChangePassword(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

    def test_change_password_success(self):

        token_url = reverse("login")

        login_data = {
            "username": "Bizhoorkhan",
            "password": "Bizh1234"
        }

        token_response = self.client.post(
            token_url,
            login_data,
            format="json"
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", token_response.data)

        access_token = token_response.data["access"]

        url = reverse("change-password")

        data = {
            "old_password": "Bizh1234",
            "new_password": "Bizhoor1234",
            "confirm_password": "Bizhoor1234"
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username="Bizhoorkhan")
        self.assertTrue(user.check_password("Bizhoor1234"))
        self.assertFalse(user.check_password("Bizh1234"))


class ProfileUpdateTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

    def test_profile_update_success(self):

        token_url = reverse("login")

        login_data = {
            "username": "Bizhoorkhan",
            "password": "Bizh1234"
        }

        token_response = self.client.post(
            token_url, 
            login_data,
            format="json"
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)

        access_token = token_response.data["access"]

        url = reverse("profile-update")

        data = {
            "username": "BizhanKhan"
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.first().username, "BizhanKhan")


class JWTTokenTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

    def test_jwt_token_success(self):

        url = reverse("login")

        data = {
            "username": "Bizhoorkhan",
            "password": "Bizh1234"
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_protected_endpoint_with_jwt(self):

        token_url = reverse("login")

        token_response = self.client.post(
            token_url,
            {
                "username": "Bizhoorkhan",
                "password": "Bizh1234"
            },
            format="json"
        )

        access_token = token_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(
            reverse("profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )