from rest_framework import serializers


class StaticsticSerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d',required=True)  #"YYYY-MM-DD"
    end_date = serializers.DateField(format='%Y-%m-%d', required=True)   #"YYYY-MM-DD"
    symbol = serializers.CharField(required=True)

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("start_date cannot be greater than end_date.")
        return data