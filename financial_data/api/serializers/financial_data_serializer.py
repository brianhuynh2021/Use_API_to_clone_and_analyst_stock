from rest_framework import serializers
from api.models.financial_data_model import FinancialDataModel

class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDataModel
        fields = ('symbol', 'date', 'open_price', 'close_price', 'volume')
