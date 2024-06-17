from rest_framework import serializers
from .models import MenuItem

class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)