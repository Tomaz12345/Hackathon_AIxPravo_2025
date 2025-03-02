from rest_framework import serializers
from .models import BrandCheck

class BrandCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandCheck
        #fields = ['id', 'brandName', 'goodsServices', 'logo']
        fields = '__all__'  # All fields are optional due to blank=True or null=True

    def validate(self, attrs):
        # Ensure at least one field is provided (brandName, goodsServices, or logo)
        if not any(attrs.get(field) for field in ['brandName', 'goodsServices', 'logo']):
            raise serializers.ValidationError('At least one of the fields (brand name, goods/services, logo) is required.')
        return attrs