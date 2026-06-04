from django.urls import path

from . import views

urlpatterns = [
    path("income/add/", views.AddIncome.as_view(), name="add-income"),
    path("income/list/", views.IncomeList.as_view(), name="list-income"),
    path("income/detail/<int:pk>/", views.IncomeDetail.as_view(), name="income-detail"),
    path("income/update/<int:pk>/", views.UpdateIncome.as_view(), name="update-income"),
    path("income/delete/<int:pk>/", views.DeleteIncome.as_view(), name="delete-income"),
]