# serializers/offer_serializer.py

from rest_framework import serializers
from listing360.models import Offer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'property', 'user', 'message', 'is_accepted', 'created_at']
