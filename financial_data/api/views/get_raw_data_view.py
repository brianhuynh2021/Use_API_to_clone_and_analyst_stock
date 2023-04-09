import os, requests
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialDataModel
from api.serializers.financial_data_serializer import FinancialDataSerializer
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
class RetrieveFinancialDataView(APIView):
    def get(self, request, symbol=None):
        api_key = API_KEY     
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({"error": "Failed to retrieve financial data"}, status=500)

        api_data = response.json().get('Time Series (Daily)', {})
        retrieve_days = 14
        # Retrieve data in 14 days
        retrieve_datas = list(api_data.items())[:retrieve_days]
        new_data = []
        for item in retrieve_datas:
            financial_data = {
                    "symbol": symbol,
                    "date": item[0],
                    "open_price": round(float(item[1].get("1. open")),2),
                    "close_price": round(float(item[1].get("4. close")),2),
                    "volume": int(item[1].get("6. volume")),
                }
            new_data.append(financial_data)
        # Insert new_data to the database if it's not exist
        for data in new_data:
            serializer = FinancialDataSerializer(data=data)
            if serializer.is_valid():
                # check record exist in database
                existing_record = FinancialDataModel.objects.filter(**serializer.validated_data).first()
                # not exist save the record
                if not existing_record:
                    serializer.save()
        # return the data that we get from API but not save all due to we may save the records before
        return Response(new_data)

# This is task for retrieve data to do task 1 - Completed task1