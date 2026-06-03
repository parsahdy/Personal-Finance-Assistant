from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password", "confirm_password", "country")

    
    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password do not match."}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "country", "avatar", "created_at")


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "Password do not match."
            )
        return attrs 