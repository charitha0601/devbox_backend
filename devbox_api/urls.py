from django.urls import path
from .views import profile_view, api_usage_get, api_usage_post

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('api-usage/', api_usage_get, name='api-usage'),
]
