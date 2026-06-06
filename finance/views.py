from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .services.dashboard import DashboardService
from .services.reports import ReportService
from .services.budgeting import BudgetService
from .models import Income, Expense, Budget, Category
from .serializers import (IncomeSerializer,
                           IncomeDetailSerializer,
                           ExpenseSerializer, 
                           ExpenseDetailSerializer, 
                           BudgetSerializer,
                           CategorySerializer)


class AddIncome(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(user=request.user)

        year = request.query_params.get("year")
        month = request.query_params.get("month")
        category = request.query_params.get("category")
        ordering = request.query_params.get("ordering")

        if year:
            incomes = incomes.filter(date__year=year)

        if month:
            incomes = incomes.filter(date__month=month)

        if category:
            incomes = incomes.filter(category__name__iexact=category)

        allowed_orderings = [
            "amount",
            "-amount",
            "date",
            "-date",
            "created_at",
            "-created_at",
        ]

        if ordering in allowed_orderings:
            incomes = incomes.order_by(ordering)
        

        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IncomeDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        income = get_object_or_404(Income, user=request.user, pk=pk)
        serializer = IncomeDetailSerializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateIncome(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        income = get_object_or_404(Income, pk=pk, user=request.user)
        serializer = IncomeSerializer(income, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteIncome(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        income = get_object_or_404(Income, pk=pk, user=request.user)
        income.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AddExpense(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExpenseList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

        year = request.query_params.get("year")
        month = request.query_params.get("month")
        category = request.query_params.get("category")
        ordering = request.query_params.get("ordering")

        if year:
            expenses = expenses.filter(date__year=year)
        
        if month:
            expenses = expenses.filter(date__month=month)

        if category:
            expenses = expenses.filter(category__name__iexact=category)

        allowed_orderings = [
            "amount",
            "-amount",
            "date",
            "-date",
            "created_at",
            "-created_at",
        ]

        if ordering in allowed_orderings:
            expenses = expenses.order_by(ordering)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ExpenseDetail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        expense = get_object_or_404(Expense, user=request.user, pk=pk)
        serializer = ExpenseDetailSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateExpense(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        expense = get_object_or_404(Expense, user=request.user, pk=pk)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteExpense(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, user=request.user, pk=pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DashboardServices(APIView): 

    permission_classes = [IsAuthenticated]

    def get(self, request):

        year = request.query_params.get("year")
        month = request.query_params.get("month")

        data = DashboardService.get_dashboard_data(
            user=request.user,
            year=year,
            month=month
        )

        return Response(data, status=status.HTTP_200_OK)



class ReportServices(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        year = request.query_params.get("year")
        month = request.query_params.get("month")

        data = ReportService.get_report_data(
            user=request.user,
            year=year,
            month=month
        )

        return Response(data, status=status.HTTP_200_OK) 
    

class AddBudgetView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BudgetListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateBudgetView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        budget = get_object_or_404(Budget, user=request.user, pk=pk)
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteBudgetView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        budget = get_object_or_404(Budget, user=request.user, pk=pk)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BudgetServices(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        year = request.query_params.get("year")
        month = request.query_params.get("month")
        category = request.query_params.get("category")

        data = BudgetService.get_budget_data(
            user=request.user,
            category=category,
            year=year,
            month=month,
        )
        return Response(data, status=status.HTTP_200_OK)
    
class AddCategory(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteCategory(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        category = get_object_or_404(Category, user=request.user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)