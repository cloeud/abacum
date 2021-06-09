from rest_framework import serializers
from .models import CSVModel

class CSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVModel
        fields = '__all__'
        
    def validate_url(self, value):
        if not value.endswith('csv'):
            raise serializers.ValidationError('Invalid URL field, it must be a CSV file')
           
        return value