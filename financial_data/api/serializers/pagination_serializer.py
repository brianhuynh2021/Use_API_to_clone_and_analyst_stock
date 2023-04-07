from rest_framework import serializers

class PaginationSerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d',required=False) #"YYYY-MM-DD"
    end_date = serializers.DateField(format='%Y-%m-%d',required=False)
    symbol = serializers.CharField(required=False)
    limit = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
     
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("start_date cannot be greater than end_date.")
        return data