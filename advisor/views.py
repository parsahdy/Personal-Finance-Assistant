from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.cache import cache

from advisor.services.chat import FinancialChatServices
from advisor.ml.predictor import LLMPredictor
from advisor.serializers import QuestionSerializer
from advisor.rag.llm_connector import llm_connector


class FinancialChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save(user=request.user)
        
        question = serializer.validated_data["question"]

        result = FinancialChatServices.chat(
            user=request.user,
            question=question
        )
        return Response ({
            "answer": result
        })
    

class FinancialForecastingView(APIView):

    parser_classes = [IsAuthenticated]

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save(user=request.user)
        
        question = serializer.validated_data["question"]

        result = LLMPredictor.forecast(
            question=question,
            user=request.user
        )
        return Response({
            "answer": result
        })
    

class  RecomendationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer.save(user=request.user)

        question = serializer.validated_data["question"]

        result = llm_connector(
            question=question,
            user=request.user,
        )
        return Response({
            "answer": result
        })