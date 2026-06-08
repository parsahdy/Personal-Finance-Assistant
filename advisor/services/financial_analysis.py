from django.db.models import Sum

from finance.models import Income, Expense
from prompts.financial_advisor import financial_advisor_prompt
from llm import ollama_client


class FinancialAnalysisService:

    @staticmethod
    def get_total_income(user, year=None, month=None):

        incomes = Income.objects.filter(user=user)

        if year:
            incomes =incomes.filter(date__year=year)

        if month:
            incomes =incomes.filter(date__month=month)

        total_income = (incomes.aggregate(total=Sum("amount"))["total"] or 0)

        return total_income
    

    @staticmethod
    def get_total_expense(user, year=None, month=None):

        expenses = Expense.objects.filter(user=user)

        if year:
            expenses =expenses.filter(date__year=year)

        if month:
            expenses =expenses.filter(date__month=month)

        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)

        return total_expense


    @staticmethod
    def get_saving_rate(user, year=None, month=None):

        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user) 

        if year:
            incomes =incomes.filter(date__year=year)
            expenses =expenses.filter(date__year=year)

        if month:
            incomes =incomes.filter(date__month=month)
            expenses =expenses.filter(date__month=month)

        total_income = (incomes.aggregate(total=Sum("amount"))["total"] or 0)
        total_expense = (expenses.aggregate(total=Sum("amount"))["total"] or 0)

        try:
            saving_rate = ((total_income - total_expense) / total_income) * 100
        except ZeroDivisionError:
            saving_rate = 0

        return saving_rate
    

    @staticmethod
    def get_largest_category(user, year=None, month=None):

        expenses = Expense.objects.filter(user=user)

        if year:
            expenses = expenses.filter(date__year=year)

        if month:
            expenses = expenses.filter(date__month=month)

        result = (
                expenses.values("category__name")
                .annotate(total_amount=Sum("amount"))
                .order_by("-total_amount")
                .first()
                )   
            
        if not result:
            return None

        return {
            "category": result["category__name"],
            "amount": result["total_amount"]
        }
    

    @staticmethod
    def get_analysis_data(user, year=None, month=None):

        return {
            "total_income": FinancialAnalysisService.get_total_income(
                user=user,
                year=year,
                month=month
            ),
            "total_expense": FinancialAnalysisService.get_total_expense(
                user=user,
                year=year,
                month=month
            ),
            "saving_rate": FinancialAnalysisService.get_saving_rate(
                user=user,
                year=year,
                month=month
            ),
            "largest_category": FinancialAnalysisService.get_largest_category(
                user=user,
                year=year,
                month=month
            ),
        }
    
    
    @staticmethod
    def analyze(user, year=None, month=None):

        data = FinancialAnalysisService.get_analysis_data(
            user=user,
            year=year,
            month=month
        )
    
        prompt_text = financial_advisor_prompt.format(
            total_income=data["total_income"],
            total_expense=data["total_expense"],
            saving_rate=round(data["saving_rate"], 2),
            largest_category=data["largest_category"],
        )

        response = ollama_client.generate(
            prompt=prompt_text
        )

        return {
            "analysis": response,
            "financial_data": data
        }