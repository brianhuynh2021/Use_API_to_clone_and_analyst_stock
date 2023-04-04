from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialData
from api.serializers.financial_data_serializer import FinancialDataSerializer
from api.utils.is_valid_start_end_dates import valid_date, valid_start_end_date


class FinancialDataView(APIView):
    """
    API view for retrieving financial data with optional filtering and pagination.

    Parameters:
        start_date (str): A string in the format YYYY-MM-DD representing the start date of the date range to filter by.
        end_date (str): A string in the format YYYY-MM-DD representing the end date of the date range to filter by.
        symbol (str): A string representing the stock symbol to filter by.
        limit (int): An integer representing the maximum number of results to return per page. Default is 5.
        page (int): An integer representing the page number of the results to return. Default is 1.

    Returns:
        A JSON object containing the financial data that match the filters, paginated according to the limit and page parameters.

    Raises:
        HTTP 404 Not Found if no financial data match the filters or if start_date is greater than end_date.
    """

    default_limit = 5

    def get(self, request):
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        symbol = request.query_params.get('symbol')
        limit = int(request.query_params.get('limit', self.default_limit))
        page = int(request.query_params.get('page', 1))

        # Query financial data with filters
        financial_data_query = FinancialData.objects.all()
        if financial_data_query.count() == 0:
            return Response({"error": "No financial data found."}, status=status.HTTP_404_NOT_FOUND)
        
        if start_date and valid_date(start_date) and end_date and valid_date(end_date):
            if valid_start_end_date(start_date, end_date) == False:
                return Response({"error": "start_date cannot be greater than end_date."}, status=status.HTTP_404_NOT_FOUND)

            financial_data_query = financial_data_query.filter(date__range=(start_date, end_date))
        elif start_date and valid_date(start_date):
            financial_data_query = financial_data_query.filter(date__gte=start_date)
        elif end_date and valid_date(end_date):
            financial_data_query = financial_data_query.filter(date__lte=end_date)

        if symbol:
            financial_data_query = financial_data_query.filter(symbol=symbol)
        
        # Paginate results
        paginator = PageNumberPagination()
        paginator.page_size = limit
        paginated_query = paginator.paginate_queryset(financial_data_query, request)

        financial_data_serializer = FinancialDataSerializer(paginated_query, many=True)

        # Return response with pagination information
        pagination = {
            'count': financial_data_query.count(),
            'page': page,
            'limit': limit,
            'pages': paginator.page.paginator.num_pages
        }

        response_data = {
            'data': financial_data_serializer.data,
            'pagination': pagination,
            'info': {'error': ''}
        }

        return Response(response_data, status=status.HTTP_200_OK)
