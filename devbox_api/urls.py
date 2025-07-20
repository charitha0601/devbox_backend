from django.urls import path
from .views import profile_view, api_usage

urlpatterns = [
    path('profile', profile_view, name='profile'),
    path('api-usage', api_usage, name='api-usage'),
]
