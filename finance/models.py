from django.db import models

from accounts.models import User


class CategoryType(models.TextChoices):
    INCOME = "income", "income"
    EXPENSE = "expense", "Expense"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    category_type = models.CharField(max_length=10, choices=CategoryType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="incomes")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="expenses")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
