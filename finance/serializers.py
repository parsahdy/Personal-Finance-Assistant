from rest_framework import serializers

from .models import Income, Expense


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = (
            "title",
            "amount",
            "description",
            "date"
        )


class IncomeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = (
            "id",
            "title",
            "amount",
            "category",
            "description",
            "date",
            "created_at",
            "updated_at",
        )


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = (
            "title",
            "amount",
            "description",
            "date"
        )


class ExpenseDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = (
            "id",
            "title",
            "amount",
            "category",
            "description",
            "date",
            "created_at",
            "updated_at",
        )
