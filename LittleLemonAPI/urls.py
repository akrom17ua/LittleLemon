from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token #Used for generating a token from an API point

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu-items/<int:id>', views.menu_item),
    path('secret/', views.secret),
    path('api-token-auth', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
]