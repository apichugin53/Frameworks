from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['owner', 'views_count']
