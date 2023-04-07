from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialDataModel
from api.serializers.financial_data_serializer import FinancialDataSerializer
from api.serializers.pagination_serializer import PaginationSerializer
from django.db.models import Q



class FinancialDataView(APIView):
    """
    APIView to retrieve financial data based on given query parameters.

    Query parameters:
    - start_date (optional): format: 'YYYY-MM-DD'
    - end_date (optional): format: 'YYYY-MM-DD'
    - symbol (optional): Symbol for the financial data such as: IBM, AAPL
    - limit (optional): Number of items to return per page (default: 5)
    - page (optional): Page number to return (default: 1)

    Returns a paginated list of financial data matching the query parameters,
    along with pagination metadata.
"""
    default_limit = 5

    def get(self, request):
        # Get query parameters
        data = {'start_date': request.query_params.get('start_date'),
                'end_date': request.query_params.get('end_date'),
                'symbol': request.query_params.get('symbol'),
                'limit': int(request.query_params.get('limit', self.default_limit)),
                'page': int(request.query_params.get('page', 1))}
        data = {key: value for key, value in data.items() if value is not None}

        serializer = PaginationSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        symbol = serializer.validated_data.get('symbol')
        limit = serializer.validated_data.get('limit')
        page = serializer.validated_data.get('page')

        # Query financial data with filters
        # We don't load all data first due to avoid the large data return
        query = Q()
        if symbol:
            query &= Q(symbol=symbol)
        if start_date and end_date:
            query &= Q(date__range=[start_date, end_date])
        elif start_date:
            query &= Q(date=start_date)
        elif end_date:
            query &= Q(date=end_date)
        get_data = FinancialDataModel.objects.filter(query)

        # Paginate results
        paginator = PageNumberPagination()
        paginator.page_size = limit
        paginated_data = paginator.paginate_queryset(get_data, request)
        pages = paginator.page.paginator.num_pages
        serializer = FinancialDataSerializer(paginated_data, many=True)

        pagination = {
            'count': get_data.count(),
            'page': page,       # current_page_index
            'limit': limit,
            'pages': pages
        }

        response_data = {
            'data': serializer.data,
            'pagination': pagination,
            'info': {'error': ''}
            }
        return Response(response_data, status=status.HTTP_200_OK)
