from rest_framework import serializers

from .models import Income


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
