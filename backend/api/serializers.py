from rest_framework import serializers
from .models import BrandCheck

class BrandCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandCheck
        fields = '__all__'
        read_only_fields = ['id', 'status', 'feedback', 'euipoResults', 'wipoResults', 'sipoResults']
