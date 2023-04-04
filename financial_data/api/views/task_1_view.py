import requests
from datetime import datetime, timedelta
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialData
from api.serializers.financial_data_serializer import FinancialDataSerializer

class RetrieveFinancialDataView(APIView):
    def get(self, request, symbol=None):
        DEFAULT_PAGE_LIMIT = 5
        two_weeks_ago = (datetime.now() - timedelta(days=14)).date()

        # check if financial data for the symbol and the last two weeks exist in the database
        existing_data = FinancialData.objects.filter(symbol=symbol, date__gte=two_weeks_ago)
        if existing_data.exists():
            serializer = FinancialDataSerializer(existing_data, many=True)
            return Response(serializer.data)

        # retrieve financial data from AlphaVantage
        api_key = "WB0DWGGXUH6PQYNG"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({"error": "Failed to retrieve financial data"}, status=500)

        api_data = response.json().get('Time Series (Daily)', {})
        new_data = []
        for date_str, daily_data in api_data.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date < two_weeks_ago:
                break
            financial_data = {
                "symbol": symbol,
                "date": date,
                "open_price": Decimal(daily_data.get("1. open")),
                "close_price": Decimal(daily_data.get("4. close")),
                "volume": int(daily_data.get("6. volume")),
            }
            new_data.append(financial_data)

        # save new financial data to database
        FinancialData.objects.bulk_create([FinancialData(**item) for item in new_data])

        # return serialized financial data
        data = new_data
        serializer = FinancialDataSerializer(data, many=True)
        return Response(serializer.data)
    
# This is for task 1