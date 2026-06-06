from django.db.models import Sum, Avg
from datetime import date

from ..models import Income, Expense



class DashboardService:

    @staticmethod
    def get_summary(user):
        
        total_income = (Income.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or 0)
        total_expense = (Expense.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or 0)
        balance = total_income - total_expense
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        }


    @staticmethod
    def get_current_month_summary(user):

        today = date.today()

        total_income = (Income.objects.filter(
                        user=user,
                        date__year=today.year,
                        date__month=today.month
                        ).aggregate(total=Sum("amount"))["total"] or 0)

        total_expense = (Expense.objects.filter(
                        user=user,
                        date__year=today.year,
                        date__month=today.month
                        ).aggregate(total=Sum("amount"))["total"] or 0)

        balance = total_income - total_expense

        return {
            "year": today.year,
            "month": today.month,
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        }
    

    @staticmethod
    def get_largest_income(user, year=None, month=None):
        
        incomes = Income.objects.filter(user=user)

        if year:
            incomes = incomes.filter(user=user, date__year=year)

        if month:
            incomes = incomes.filter(user=user, date__month=month)

        largest_income = incomes.order_by("-amount", "-date", "-id").first()

        return {
            "year": year,
            "month": month,
            "title": largest_income.title,
            "amount": largest_income.amount,
            "category": largest_income.category.name if largest_income.category else None,        
            }

    
    @staticmethod
    def get_lowest_income(user, year=None, month=None):
        
        incomes = Income.objects.filter(user=user)

        if year:
            incomes = incomes.filter(user=user, date__year=year)

        if month:
            incomes = incomes.filter(user=user, date__month=month)

        lowest_income = incomes.order_by("amount", "-date", "-id").first()

        return {
            "year": year,
            "month": month,
            "title": lowest_income.title,
            "amount": lowest_income.amount,
            "category": lowest_income.category.name if lowest_income.category else None,        
            }
    

    @staticmethod
    def get_largest_expense(user, year=None, month=None):
        
        expenses = Expense.objects.filter(user=user)

        if year:
            expenses = expenses.filter(user=user, date__year=year)

        if month:
            expenses = expenses.filter(user=user, date__month=month)

        largest_expense = expenses.order_by("-amount", "-date", "-id").first()

        return {
            "year": year,
            "month": month,
            "title": largest_expense.title,
            "amount": largest_expense.amount,
            "category": largest_expense.category.name if largest_expense.category else None,        
            }
    

    @staticmethod
    def get_lowest_expense(user, year=None, month=None):
        
        expenses = Expense.objects.filter(user=user)

        if year:
            expenses = expenses.filter(user=user, date__year=year)

        if month:
            expenses = expenses.filter(user=user, date__month=month)

        lowest_expense = expenses.order_by("-amount", "-date", "-id").first()

        return {
            "year": year,
            "month": month,
            "title": lowest_expense.title,
            "amount": lowest_expense.amount,
            "category": lowest_expense.category.name if lowest_expense.category else None,        
        }

    

    @staticmethod
    def get_expense_income_ratio(user, year=None, month=None):
        
        incomes = Income.objects.filter(user=user)
        expenses =Expense.objects.filter(user=user)

        if year:
            incomes = incomes.filter(user=user, date__year=year)
            expenses = expenses.filter(user=user, date__year=year)

        if month:
            incomes = incomes.filter(user=user, date__month=month)
            expenses = expenses.filter(user=user, date__month=month)

        total_income = (incomes.aggregate(total=Sum("amount"))["total"] or 0)
        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)

        try:    
            expense_income_ratio = (total_expense / total_income) * 100
        except ZeroDivisionError:
            expense_income_ratio = 0

        return {
            "expense_income_ratio": expense_income_ratio
        }
    

    @staticmethod
    def get_saving_rate(user, year=None, month=None):
        
        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)

        if year:
            incomes = incomes.filter(date__year=year)
            expenses = expenses.filter(date__year=year)

        if month:
            incomes = incomes.filter(date__month=month)
            expenses = expenses.filter(date__month=month)

        total_income = (incomes.aggregate(total=Sum("amount"))["total"] or 0)
        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)

        try:
            saving_rate = ((total_income - total_expense) / total_income) * 100
        except ZeroDivisionError:
            saving_rate = 0


        return {
            "year": year,
            "month": month,
            "total_income": total_income,
            "total_expense": total_expense,
            "saving_rate": round(saving_rate, 2)
        }
    

    @staticmethod
    def get_dashboard_data(user, year=None, month=None):

        return {
            "summary": DashboardService.get_summary(user),
            "current_month_summary": DashboardService.get_current_month_summary(user),
            "largest_income": DashboardService.get_largest_income(user, year, month),
            "lowest_income": DashboardService.get_lowest_income(user, year, month),
            "largest_expense": DashboardService.get_lowest_expense(user, year, month),
            "saving_rate": DashboardService.get_saving_rate(user, year, month),
            "expense_income_ratio": DashboardService.get_expense_income_ratio(user, year, month),
        }
