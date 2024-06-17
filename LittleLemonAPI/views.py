from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def menuitems(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_data = MenuItemSerializer(items, many=True)
    return Response(serialized_data.data)

@api_view()
def menuitem(request, id):
    item = MenuItem.objects.get(pk=id)
    serialized_data = MenuItemSerializer(item)
    return Response(serialized_data.data)
