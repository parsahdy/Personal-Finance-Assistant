from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.cache import cache

from advisor.services.chat import FinancialChatServices
from advisor.serializers import QuestionSerializer


class FinancialChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = serializer.validated_data["question"]

        result = FinancialChatServices.chat(
            user=request.user,
            question=question
        )
        return Response ({
            "answer": result
        })