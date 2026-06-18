from django.test import TestCase

from accounts.models import User
from ..models import Income, Expense, Category
from ..services.dashboard import DashboardService

class TestDashboardService(TestCase):

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

        self.food_category = Category.objects.create(
            name="Food"
        )

        self.car_category = Category.objects.create(
            name="Car"
        )

        self.income1 = Income.objects.create(
            user = self.user,
            title = "Paycheck",
            amount = 2000,
            description = "This month company paycheck.",
            category = self.work_category,
            date = "2026-10-01"
        )

        self.income2 = Income.objects.create(
            user = self.user,
            title = "Bounes",
            amount = 800,
            description = "Extra work bounes.",
            category = self.work_category,
            date = "2026-11-11"
        )

        self.expense1 = Expense.objects.create(
            user = self.user,
            title = "Resturant",
            amount = 200,
            description = "A nice meal with friends.",
            category = self.food_category,
            date = "2026-11-22"
        )

        self.expense2 = Expense.objects.create(
            user = self.user,
            title = "Tiers",
            amount = 350,
            description = "Buying new tiers for my pickup.",
            category = self.car_category,
            date = "2026-08-22"
        )

    def test_get_summary(self):

        result = DashboardService.get_summary(
            user=self.user
        )

        self.assertEqual(result["total_income"], 2800)
        self.assertEqual(result["total_expense"], 550)