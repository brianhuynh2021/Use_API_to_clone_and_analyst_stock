from django.urls import reverse
from rest_framework.test import APITestCase
from api.models.financial_data_model import FinancialDataModel


class FinancialDataViewTestCase(APITestCase):
    def setUp(self):
        # Create some FinancialDataModel objects for testing
        FinancialDataModel.objects.create(symbol='AAPL', date='2023-03-01', open_price=150.0, close_price=148.0, volume=17000)
        FinancialDataModel.objects.create(symbol='AAPL', date='2023-04-06', open_price=124.0, close_price=148.0, volume=23400)
        FinancialDataModel.objects.create(symbol='IBM', date='2023-03-01', open_price=120.0, close_price=125.0, volume=32000)
        FinancialDataModel.objects.create(symbol='IBM', date='2023-04-06', open_price=122.0, close_price=124.0, volume=31000)

    def test_get_financial_data_with_symbol_filter(self):
        # Test filtering by symbol
        url = reverse('financial-data')
        response = self.client.get(url, {'symbol': 'AAPL'})
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['symbol'], 'AAPL')
        self.assertEqual(response.data['pagination']['page'], 1)
