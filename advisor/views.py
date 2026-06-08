from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from services.financial_analysis import FinancialAnalysisService


class FinancialAnalyzeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        year = request.query_params.get("year")
        month = request.query_params.get("month")

        try:
            analysis = FinancialAnalysisService.analyze(
                user=request.user,
                year=year,
                month=month
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(analysis, status=status.HTTP_200_OK)