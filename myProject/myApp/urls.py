from django.db import router
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('signup/', views.signup_view.as_view(), name='signup'),
    path('login/',views.Login_view.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('Updat_password/',views.change_password.as_view(),name='logout'),
    path('add_user/',views.add_user, name='Add_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('search_user/', views.search_user, name='search_user'),

    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),


]