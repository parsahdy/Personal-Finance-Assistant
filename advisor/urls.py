from django.urls import path

from . import views 


urlpatterns = [
    path("chat/", views.FinancialChatView.as_view(), name="financial-chat"),
    path("forecast/", views.FinancialForecastingView.as_view(), name="financial-forecast"),
]