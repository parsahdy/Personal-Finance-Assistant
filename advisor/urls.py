from django.urls import path

from . import views 


urlpatterns = [
    path("analyze/", views.FinancialAnalyzeView.as_view(), name="financial-analyze"),
]