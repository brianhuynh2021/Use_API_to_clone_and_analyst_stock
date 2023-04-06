from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialDataModel
from api.utils.is_valid_start_end_dates import valid_date, valid_start_end_date


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
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        symbols = request.query_params.get('symbols')

        # Validate query parameters
        if not start_date or not valid_date(start_date):
            return Response({'info': {'error': 'start_date parameter is invalid or missing'}}, status=status.HTTP_400_BAD_REQUEST)
        if not end_date or not valid_date(end_date):
            return Response({'info': {'error': 'end_date parameter is invalid or not missing'}}, status=status.HTTP_400_BAD_REQUEST)
        if valid_start_end_date(start_date, end_date) == False:
            return Response({'info': {'error': 'end_date cannot be less than start_date'}}, status=status.HTTP_404_NOT_FOUND)
        if not symbols:
            return Response({'info': {'error': 'symbols parameter is missing'}}, status=status.HTTP_400_BAD_REQUEST)

        # Parse symbols parameter
        symbol_list = symbols.split(',')

        # Query financial data with filters
        financial_data_query = FinancialDataModel.objects.filter(symbol__in=symbol_list, date__range=(start_date, end_date))
        if financial_data_query.count() == 0:
            return Response({"info": {"error": "No financial data found."}}, status=status.HTTP_404_NOT_FOUND)
        # Calculate statistics for each symbol
        statistics = {}
        for symbol in symbol_list:
            symbol_data = financial_data_query.filter(symbol=symbol)
            if symbol_data.count() > 0:
                open_prices = [data.open_price for data in symbol_data]
                close_prices = [data.close_price for data in symbol_data]
                volumes = [data.volume for data in symbol_data]
                statistics[symbol] = {
                    'average_daily_open_price': sum(open_prices) / len(open_prices),
                    'average_daily_close_price': sum(close_prices) / len(close_prices),
                    'average_daily_volume': sum(volumes) / len(volumes)
                }

        # Return response
        response_data = {
            'data': statistics,
            'info': {'error': ''}
        }
        return Response(response_data, status=status.HTTP_200_OK)
