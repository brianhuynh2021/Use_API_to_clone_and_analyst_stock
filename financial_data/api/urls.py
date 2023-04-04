from django.urls import path
from api.views.task_1_view import RetrieveFinancialDataView
from api.views.financial_data_view import FinancialDataView
from api.views.staticstics_view import StatisticsView

urlpatterns = [
    path('retrieve_financial_data/<str:symbol>/', RetrieveFinancialDataView.as_view(), name='get-financial-data'),
    path('financial_data', FinancialDataView.as_view(), name='financial-data'),
    path('statistics', StatisticsView.as_view(), name='staticstics')
]