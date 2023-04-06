from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.financial_data_model import FinancialDataModel
from api.serializers.financial_data_serializer import FinancialDataSerializer
from api.serializers.pagination_serializer import PaginationSerializer


class FinancialDataView(APIView):

    default_limit = 5

    def get(self, request):
        # Get query parameters
        data = {'start_date': request.query_params.get('start_date'),
                'end_date': request.query_params.get('end_date'),
                'symbol': request.query_params.get('symbol'),
                'limit': int(request.query_params.get('limit', self.default_limit)),
                'page': int(request.query_params.get('page', 1))}
        print("data==>", data)
        serializer = PaginationSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        symbol = serializer.validated_data.get('symbol')
        limit = serializer.validated_data.get('limit')
        page = serializer.validated_data.get('page')
        # Query financial data with filters
        get_data = [] # Here we don't load all data like FinancialDataModel.objects.filter.all() consider large data as 1 million
        if symbol:
            get_data.append(FinancialDataModel.objects.filter(symbol=symbol))
        if start_date and end_date:
            if start_date > end_date:
                return Response({"error": "start_date cannot be greater than end_date."}, status=status.HTTP_400_BAD_REQUEST)
            get_data = FinancialDataModel.objects.filter(date__range=[start_date, end_date])
        elif start_date or end_date:
            get_data = FinancialDataModel.objects.filter(date=start_date) | FinancialDataModel.objects.filter(date=end_date)
        else:
            get_data = FinancialDataModel.objects.all()
        get_data = FinancialDataSerializer(get_data, many=True)
        # Paginate results
        paginator = PageNumberPagination()
        paginator.page_size = limit
        # paginated_query = paginator.paginate_queryset(financial_data_query, request)

        # financial_data_serializer = FinancialDataSerializer(paginated_query, many=True)

        # Return response with pagination information
        # pagination = {
        #     'count': financial_data_query.count(),
        #     'page': page,
        #     'limit': limit,
        #     'pages': paginator.page.paginator.num_pages
        # }

        # response_data = {
        #     'data': serializer.data,
        #     'pagination': pagination,
        #     'info': {'error': ''}
        # }
        return Response({"data": get_data.data}, status=status.HTTP_200_OK)
