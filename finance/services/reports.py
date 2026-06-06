from django.db.models import Sum, Avg
from datetime import date

from ..models import Income, Expense



class ReportService:

    @staticmethod
    def _get_summary(user, year=None, month=None):

        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)

        if year:
            incomes = Income.objects.filter(user=user, date__year=year)
            expenses = Expense.objects.filter(user=user, date__year=year)
        
        if month:
            incomes = Income.objects.filter(user=user, date__month=month)
            expenses = Expense.objects.filter(user=user, date__month=month)

        total_income = (incomes.aggregate(total=Sum("amount"))["total"] or 0)
        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)
        balance = total_income - total_expense
        largest_income = (incomes.order_by("-amount", "-date", "-id")).first()
        lowest_income = (incomes.order_by("amount", "-date", "-id")).first()
        largest_expense = (expenses.order_by("-amount", "-date", "-id")).first()
        lowest_expense =  (expenses.order_by("amount", "-date", "-id")).first()

        return {
            "year": year,
            "month": month,
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "largest_income": {
                "title": largest_income.title,
                "amount": largest_income.amount
            },
            "lowest_income": {
                "title": lowest_income.title,
                "amount": lowest_income.amount
            },
            "largest_expense": {
                "title": largest_expense.title,
                "amount": largest_expense.amount
            },
            "lowest_expense": {
                "title": lowest_expense.title,
                "amount": lowest_expense.amount
            },
            
        }

    @staticmethod
    def get_yearly_summary(user, year=None):

        return ReportService._get_summary(user=user, year=year)
    

    @staticmethod
    def get_monthly_summary(user, month=None):
       
        return ReportService._get_summary(user=user, month=month)


    @staticmethod
    def get_expense_by_category(user, category=None):
        
        expenses = Expense.objects.filter(user=user)

        if not category:
            return {
                "error": "Category is required."
            }
        else:
            expenses = expenses.filter(category=category)

        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)

        return {
            f"total expense by category {category}": total_expense
        }


    @staticmethod
    def get_income_by_category(user, category=None):
        incomes = Income.objects.filter(user=user)

        if not category:
            return None
        else:
            incomes = incomes.filter(category=category)

        total_income = (incomes.aggregate(total=Sum("amount"))["total"] or 0)

        return {
            f"total income by category {category}": total_income
        }


    @staticmethod
    def get_average_daily_expense(user, year=None, month=None):

        if not year or not month:
            return{
                "error": "year and month are required."
            }

        expenses = Expense.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )

        average_expense = (expenses.aggregate(average=Avg("amount"))["average"] or 0)

        return {
            "Today average expense": average_expense
        }
    

    @staticmethod
    def get_report_data(user, year=None, month=None):

        return {
            "yearly_summary": ReportService.get_yearly_summary(user, year),
            "monthly_summary": ReportService.get_monthly_summary(user, month),
            "expense_by_category": ReportService.get_expense_by_category(user, category=None),
            "income_by_category": ReportService.get_income_by_category(user, category=None),
            "average_daily_expense": ReportService.get_average_daily_expense(user, year, month),
        }