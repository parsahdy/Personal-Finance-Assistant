from celery import shared_task
from openpyxl import Workbook
from django.conf import settings
import csv
import os

from accounts.models import User
from .models import Income, Expense


EXPORT_DIR = os.path.join(settings.MEDIA_ROOT, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

@shared_task
def generate_income_csv(user_id, year=None, month=None):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise User.DoesNotExist(
            f"User {user_id} not found."
        )
    
    incomes = Income.objects.filter(user=user)

    if year:
        incomes = incomes.filter(date__year=year)

    if month:
        incomes = incomes.filter(date__month=month)

    filename = f"income_csv_{user_id}_{year}_{month}"
    filepath = os.path.join(EXPORT_DIR, f"{filename}.csv")
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Title",
            "Amount",
            "Description",
            "Category",
            "date"
        ])

        for income in incomes:
            writer.writerow([
                income.title,
                float(income.amount),
                income.description,
                income.category.name if income.category else "",
                str(income.date)
            ]) 

    return filepath


@shared_task
def generate_expense_csv(user_id, year=None, month=None):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise User.DoesNotExist (
            f"User {user_id} not found."
        )
    
    expenses = Expense.objects.filter(user=user)

    if year:
        expenses = expenses.filter(date__year=year)
    
    if month:
        expenses = expenses.filer(date__month=month)

    filename = f"expense_{user_id}_{year}_{month}"
    filepath = os.path.join(EXPORT_DIR, f"{filename}.csv")

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Title",
            "Amount",
            "Description",
            "Category",
            "date"
        ])

        for expense in expenses:
            writer.writerow([
                expense.title,
                float(expense.amount),
                expense.description,
                expense.category.name if expense.category else "",
                str(expense.date)
            ])

@shared_task
def generate_income_xlsx(user_id, year=None, month=None):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise User.DoesNotExist(
            f"User {user_id} not found."
        )
    
    incomes = Income.objects.filter(user=user)

    if year:
        incomes = incomes.filter(date__year=year)

    if month:
        incomes = incomes.filter(date__month=month)

    wb = Workbook()
    ws = wb.active
    ws.title = "Incomes"

    ws.append([
        "Title",
        "Amount",
        "Description",
        "Category",
        "date"
    ])
    
    for income in incomes:
        ws.append([
            income.title,
            float(income.amount),
            income.description,
            income.category.name if income.category else "",
            income.date
        ])
    

    filename = f"Income_xlsx_{user_id}_{year}_{month}"
    filepath = os.path.join(EXPORT_DIR, f"{filename}.xlsx")
    wb.save(filepath)
    return filepath


@shared_task
def generate_expense_xlsx(user_id, year=None, month=None):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise User.DoesNotExist(
            f"User {user_id} not found."
        )
    
    expenses = Expense.objects.filter(user=user)

    if year:
        expenses = expenses.filter(date__year=year)

    if month:
        expenses = expenses.filter(date__month=month)

    wb = Workbook()
    ws = wb.active
    ws.title = "Expense"

    ws.append([
        "Title",
        "Amount",
        "Description",
        "Category",
        "date"
    ])
    
    for expense in expenses:
        ws.append([
            expense.title,
            float(expense.amount),
            expense.description,
            expense.category.name if expense.category else "",
            expense.date
        ])
    
    filename = f"Income_xlsx_{user_id}_{year}_{month}"
    filepath = os.path.join(EXPORT_DIR, f"{filename}.xlsx")

    ws.save(filepath)
    return filepath