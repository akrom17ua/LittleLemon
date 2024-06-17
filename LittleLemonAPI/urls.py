from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
]