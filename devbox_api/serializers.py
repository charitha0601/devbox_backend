from rest_framework import serializers

class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()

class APIUsageSerializer(serializers.Serializer):
    endpoint = serializers.CharField()
    method = serializers.CharField()
    timestamp = serializers.DateTimeField()