from django.urls import path

from . import views

urlpatterns = [
    path("income/add/", views.AddIncome.as_view(), name="add-income"),
    path("income/list/", views.IncomeList.as_view(), name="list-income"),
    path("income/detail/<int:pk>/", views.IncomeDetail.as_view(), name="income-detail"),
    path("income/update/<int:pk>/", views.UpdateIncome.as_view(), name="update-income"),
    path("income/delete/<int:pk>/", views.DeleteIncome.as_view(), name="delete-income"),

    path("expense/add/", views.AddExpense.as_view(), name="add-expense"),
    path("expense/list/", views.ExpenseList.as_view(), name="list-expense"),
    path("expense/detail/<int:pk>/", views.ExpenseDetail.as_view(), name="expense-detail"),
    path("expense/update/<int:pk>/", views.UpdateExpense.as_view(), name="update-expense"),
    path("expense/delete/<int:pk>/", views.DeleteExpense.as_view(), name="delete-expens"),
]