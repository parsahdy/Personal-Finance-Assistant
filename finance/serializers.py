from rest_framework import serializers

from .models import Income, Expense, Budget, Category


class IncomeSerializer(serializers.ModelSerializer):

    category = serializers.CharField(
        required=False, 
        allow_blank=True, 
        allow_null=True
    )

    class Meta:
        model = Income
        fields = (
            "title",
            "amount",
            "description",
            "category",
            "date"
        )

    def create(self, validated_data):
        category_name = validated_data.pop("category", None)
        category, _ = Category.objects.get_or_create(name=category_name)
        validated_data["category"] = category
        return Income.objects.create(**validated_data)


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

    category = serializers.CharField(
        required=False,
        allow_blank=True, 
        allow_null=True
    )

    class Meta:
        model = Expense
        fields = (
            "title",
            "amount",
            "description",
            "category",
            "date"
        )

    def create(self, validated_data):
        category_name = validated_data.pop("category", None)
        category, _ = Category.objects.get_or_create(name=category_name)
        validated_data["category"] = category
        return Expense.objects.create(**validated_data)


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


    
class BudgetSerializer(serializers.ModelSerializer):
 
    category = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Budget
        fields = (
            "category",
            "limit_amount",
            "date"
        )

    def create(self, validated_data):
        category_name = validated_data.pop("category", None)
        category, _ = Category.objects.get_or_create(name=category_name)
        validated_data["category"] = category
        return Budget.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "category_type"
        )