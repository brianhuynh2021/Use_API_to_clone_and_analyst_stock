from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialDataModel


class StatisticsView(APIView):
    """
    API view for calculating statistics on financial data within a date range.

    Parameters:
        start_date (str): A string in the format YYYY-MM-DD representing the start date of the date range to calculate statistics for. Required.
        end_date (str): A string in the format YYYY-MM-DD representing the end date of the date range to calculate statistics for. Required.
        symbols (str): A comma-separated string representing the stock symbols to calculate statistics for. Required.

    Returns:
        A JSON object containing the calculated statistics for each symbol within the date range.

    Raises:
        HTTP 400 Bad Request if any required parameters are missing or invalid.
        HTTP 404 Not Found if no financial data match the filters.
    """

    def get(self, request):
        # Get query parameters
        response_data = "Hello world"
        return Response(response_data, status=status.HTTP_200_OK)
