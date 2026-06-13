from django.db.models import Sum
from django.db.models.functions import TruncMonth

from finance.models import Income, Expense

class ForecastingService:
    
    @staticmethod
    def get_income_time_series(user):

        incomes = (
            Income.objects
            .filter(user=user)
            .annotate(period=TruncMonth("date"))
            .values("period")
            .annotate(income=Sum("amount"))
            .order_by("period")
        )

        return list(incomes)
    

    @staticmethod
    def get_expense_time_series(user):

        expenses = (
            Expense.objects
            .filter(user=user)
            .annotate(period=TruncMonth("date"))
            .values("period")
            .annotate(expense=Sum("amount"))
            .order_by("period")
        )

        return list(expenses)


    @staticmethod
    def get_saving_time_series(incomes, expenses):
        
        income_map = {
            (item["period"]): item["income"]
            for item in incomes
        }

        expense_map = {
            (item["period"]): item["expense"]
            for item in expenses
        }

        all_keys = sorted(set(income_map.keys()) | set(expense_map.keys()))

        result = []

        for period in all_keys:
            income = income_map.get((period), 0)
            expense = expense_map.get((period), 0)

            if income != 0:
                saving_rate = ((income - expense) / income) * 100
            else:
                saving_rate = 0

            result.append({
                "period": period,
                "saving_rate": round(saving_rate, 2)
            })
        
        return result