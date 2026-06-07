from django.http import HttpResponse
from openpyxl import Workbook
import csv

from ..models import Expense, Income


class ExpoertService:

    @staticmethod
    def export_income_csv(user, year=None, month=None):

        incomes = Income.objects.filter(user=user)

        if year:
            incomes = incomes.filter(date__year=year)

        if month:
            incomes = incomes.filter(date__month=month)

        response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="income_report.csv"'} 
            )
        
        writer = csv.writer(response)
        writer.writerow([
            "Title",
            "Amount",
            "Category",
            "Description",
            "Date"
        ])

        for income in incomes:
            writer.writerow([
                income.title,
                float(income.amount),
                income.category if income.category else "",
                income.description,
                str(income.date),
            ])

        return response

    
    @staticmethod
    def export_expense_csv(user, year=None, month=None):

        expenses = Expense.objects.filter(user=user)

        if year:
            expenses = expenses.filter(date__year=year)

        if month:
            expenses = expenses.filter(date__month=month)

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="expense_income.csv"'}
        )

        writer = csv.writer(response)
        writer.writerow([
            "Title",
            "Amount",
            "Category",
            "Description",
            "Date"
        ])

        for expense in expenses:
            writer.writerow([
                expense.title,
                float(expense.amount),
                expense.category if expense.category else "",
                expense.description,
                str(expense.date),
            ])
        
        return response


    @staticmethod
    def export_income_xlsx(user, year=None, month=None):

        incomes = Income.objects.filter(user=user)

        if year:
            incomes = incomes.filter(date__year=year)

        if month:
            incomes = incomes.filter(date__month=month)

        wb = Workbook()
        ws = wb.active
        ws.title = "Incomes"

        ws.append =([
            "Title",
            "Amount",
            "Category",
            "Description",
            "Date"
        ])

        for income in incomes:
            ws.append([
                income.title,
                float(income.amount),
                income.category if income.category else "",
                income.description,
                str(income.date)
            ])

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        )

        response["Content-Disposition"] = (
            'attachment; filename="income_report.xlsx"'
        )

        wb.save(response)

        return response
        


    
    @staticmethod
    def export_expense_xlsx(user, year=None, month=None):

        expenses = Expense.objects.filter(user=user)

        if year:
            expenses = expenses.filter(date__year=year)

        if month:
            expenses = expenses.filter(date__month=month)

        wb = Workbook()
        ws = wb.active
        ws.title = "Expenses"

        ws.append([
            "Title",
            "Amount",
            "Category",
            "Description",
            "Date",
        ])

        for expense in expenses:
            ws.append([
                expense.title,
                float(expense.amount),
                expense.category.name if expense.category else "",
                expense.description,
                str(expense.date),
            ])

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        )

        response["Content-Disposition"] = (
            'attachment; filename="expense_report.slsx"'
        )

        wb.save(response)

        return response