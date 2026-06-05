from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from .models import Income, Expense
from .serializers import IncomeSerializer, IncomeDetailSerializer, ExpenseSerializer, ExpenseDetailSerializer


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

        if year:
            incomes = Income.objects.filter(date__year=year)

        if month:
            incomes = Income.objects.filter(date__month=month)

        if category:
            incomes = Income.objects.filter(category__name__iexact=category)

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

        if year:
            expenses = Expense.objects.filter(date__year=year)
        
        if month:
            expenses = Expense.objects.filter(date__month=month)

        if category:
            expenses = Expense.objects.filter(category__name__iexact=category)

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