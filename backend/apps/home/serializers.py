from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from .models import FavoriteSearch

class FavoriteSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteSearch
        fields = '__all__'