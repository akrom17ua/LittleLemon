from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.menuitems),
    path('menu-items/<int:pk>', views.menuitem),
]