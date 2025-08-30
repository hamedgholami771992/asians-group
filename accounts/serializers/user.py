from rest_framework import serializers
from accounts.models import User

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    Includes password (write-only).
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        # ✅ Ensure password is hashed
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            password=validated_data["password"],
        )
        return user
    


class UserSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for displaying user info (no password).
    """
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username", "email"]