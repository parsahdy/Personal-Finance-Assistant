from django.db.models import Sum, Avg
from datetime import date

from ..models import Income, Expense, Budget



class BudgetService:

    @staticmethod
    def budget_status(user, category,  year=None, month=None):
        
        budgets = Budget.objects.filter(user=user, category__name=category)

        if year:
            budgets = budgets.filter(date__year=year)

        if month:
            budgets = budgets.filter(date__month=month)
        
        status = budgets.aggregate(
            total=Sum("limit_amount"),
            average=Avg("limit_amount")
            )

        return {
            "total_budget": status["total"],
            "average_budget": status["average"]
        }


    @staticmethod
    def remaining_budget(user, category):
        
        today = date.today()

        budgets = Budget.objects.filter(
            user=user,
            category__name=category, 
            date__year=today.year,
            date__month=today.month
        )

        expenses = Expense.objects.filter(
            user=user, 
            category__name=category,
            date__year=today.year,
            date__month=today.month
        )

        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)
        total_budget = (budgets.aggregate(total=Sum("limit_amount"))["total"] or 0)
        remaining_budget = total_budget - total_expense

        if remaining_budget <= 0:
            return {
            "remaining_budget": remaining_budget,
            "is_over_budget": True
            }
        
        return {
            "remaing_budget": remaining_budget,
            "is_over_budget": False
        }

    @staticmethod
    def get_budget_data(user, category, year=None, month=None):

        return {
            "budget_status": BudgetService.budget_status(
                user=user,
                year=year,
                month=month,
                category=category
            ),
            "remaining_budget": BudgetService.remaining_budget(
                user=user,
                category=category
            ),
        }
    