from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer, APIUsageSerializer
from datetime import datetime
import pytz
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Data
MOCK_PROFILE = {
    "username": "devbox",
    "email": "devbox@example.com",
    "full_name": "Devbox User"
}

MOCK_API_USAGE = [
    {"endpoint": "/profile", "method": "GET", "timestamp": datetime.now(pytz.utc)},
    {"endpoint": "/api-usage", "method": "GET", "timestamp": datetime.now(pytz.utc)},
]

# Simulate Kafka event logging
def log_event_to_kafka(event, user=None):
    try:
        user_info = f" | user: {user.username}" if user else ""
        logger.info(f"[Kafka Simulation] {datetime.utcnow().isoformat()} | Event: {event}{user_info}")
    except Exception as e:
        logger.error(f"Failed to log event to Kafka: {e}")


# GET /profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = UserProfileSerializer(MOCK_PROFILE)
    return Response(serializer.data)

# GET /api-usage
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_usage(request):
    """
    GET: Returns mock API usage data.
    POST: Adds a new API usage entry and logs the event.
    """
    if request.method == 'GET':
        serializer = APIUsageSerializer(MOCK_API_USAGE, many=True)
        # Log the GET event to Kafka
        log_event_to_kafka("API usage GET requested", request.user)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = APIUsageSerializer(data=request.data)
        if serializer.is_valid():
            MOCK_API_USAGE.append(serializer.validated_data)
            # Log the event to Kafka
            log_event_to_kafka(f"API usage logs {serializer.validated_data}", request.user)
            return Response({"message": "API usage logged successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

