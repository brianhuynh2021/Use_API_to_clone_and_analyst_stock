from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.staticstic_serializer import StaticsticSerializer 
from api.models.financial_data_model import FinancialDataModel
from django.db.models import Avg


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
        # Validate input parameters
        serializer = StaticsticSerializer(data={
                "start_date": request.query_params.get("start_date"),
                "end_date": request.query_params.get("end_date"),
                "symbol": request.query_params.get("symbol")
            })
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Filter data based on input parameters
        queryset = FinancialDataModel.objects.filter(
            symbol=validated_data["symbol"],
            date__gte=validated_data["start_date"],
            date__lte=validated_data["end_date"]
        )
        
        # Calculate statistics
        average_daily_open_price = queryset.aggregate(Avg('open_price'))['open_price__avg']
        average_daily_close_price = queryset.aggregate(Avg('close_price'))['close_price__avg']
        average_daily_volume = queryset.aggregate(Avg('volume'))['volume__avg']
        
        # Construct response
            
        data = {
                "start_date": validated_data["start_date"],
                "end_date": validated_data["end_date"],
                "symbol": validated_data["symbol"],
                "average_daily_open_price": average_daily_open_price,
                "average_daily_close_price": average_daily_close_price,
                "average_daily_volume": average_daily_volume
            }
        response = {
            "data": data,
            "info": ""
        }
        return Response(response, status=status.HTTP_200_OK)
