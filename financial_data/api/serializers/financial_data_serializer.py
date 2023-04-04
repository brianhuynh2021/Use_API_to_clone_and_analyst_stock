from rest_framework import serializers
from api.models.financial_data_model import FinancialData

class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = ('symbol', 'date', 'open_price', 'close_price', 'volume')
