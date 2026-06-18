from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User
from ..models import Income, Expense, Category


class TestAddIncome(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

        self.work_category = Category.objects.create(
            name="Work"
        )

    def test_add_income_success(self):

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

        url = reverse("add-income")

        data = {
            "title": "Paycheck",
            "amount": 2000,
            "description": "This month company paycheck.",
            "category": self.work_category.id,
            "date": "2026-06-18",
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Income.objects.first().title, "Paycheck")


class TestUpdateIncome(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

        self.work_category = Category.objects.create(
            name="Work"
        )

        self.income = Income.objects.create(
            user = self.user,
            title = "Paycheck",
            amount = 2000,
            description = "This month company paycheck.",
            category = self.work_category,
            date = "2026-10-01"
        )


    def test_update_income_success(self):

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

        url = reverse("update-income", args=[self.income.id])

        data = {
            "amount": 3000,
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
        self.assertEqual(Income.objects.first().amount, 3000)
        self.assertNotEqual(Income.objects.first().amount, 2000)


class TestDeleteIncome(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

        self.work_category = Category.objects.create(
            name="Work"
        )

        self.income = Income.objects.create(
            user = self.user,
            title = "Paycheck",
            amount = 2000,
            description = "This month company paycheck.",
            category = self.work_category,
            date = "2026-10-01"
        )

    def test_delete_income(self):

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

        url = reverse("delete-income", args=[self.income.id])

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.delete(url)
  
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Income.objects.filter(pk=self.income.pk).exists())


class TestAddExpense(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

        self.food_category = Category.objects.create(
            name="Foos"
        )

    def test_add_expense_success(self):

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

        url = reverse("add-expense")

        data = {
            "title": "Resturant",
            "amount": 200,
            "description": "A nice meal with friends.",
            "category": self.food_category.id,
            "date": "2026-03-10",
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().title, "Resturant")


class TestUpdateExpense(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

        self.food_category = Category.objects.create(
            name="Food"
        )

        self.expense = Expense.objects.create(
            user = self.user,
            title = "Resturant",
            amount = 200,
            description = "A nice meal with friends.",
            category = self.food_category,
            date = "2026-11-22"
        )

    def test_update_expense_success(self):

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

        url = reverse("update-expense", args=[self.expense.id])

        data = {
            "amount": 400,
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
        self.assertEqual(Expense.objects.first().amount, 400)
        self.assertNotEqual(Expense.objects.first().amount, 200)


class TestDeleteExpense(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "Bizhan",
            last_name = "Mozi",
            username = "Bizhoorkhan",
            email = "Bizhoorkhan@gmail.com",
            password = "Bizh1234",
            country = "Iran"
        )

        self.food_category = Category.objects.create(
            name="Food"
        )

        self.expense = Expense.objects.create(
            user = self.user,
            title = "Resturant",
            amount = 200,
            description = "A nice meal with friends.",
            category = self.food_category,
            date = "2026-11-22"
        )

    def test_delete_expense(self):

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

        url = reverse("delete-expense", args=[self.expense.id])

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.delete(url)
  

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(pk=self.expense.pk).exists())