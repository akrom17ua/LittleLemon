from logging import Manager
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from .throttles import TenCallsPerMinute
from django.contrib.auth.models import User, Group



@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price_lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def menu_item(request, id):
    item = get_object_or_404(MenuItem,pk=id)
    serialized_data = MenuItemSerializer(item)
    return Response(serialized_data.data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Only manager should see this"})
    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})



@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle]) #you can user TenCallsPerMinute throttler here as well
def throttle_check_auth(request):
    return Response({"message": "message for the logged in users only"})


@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data["username"]
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        if request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "ok"})

    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)