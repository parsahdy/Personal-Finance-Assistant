from rest_framework import serializers

from advisor.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ("question",)