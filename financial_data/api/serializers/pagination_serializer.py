from rest_framework import serializers

class PaginationSerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d',required=False) #"YYYY-MM-DD"
    end_date = serializers.DateField(format='%Y-%m-%d',required=False)
    symbol = serializers.CharField(required=False)
    limit = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
     