# users/serializers.py
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2", "first_name", "last_name")
        read_only_fields = ("id",)

    def validate(self, attrs):
        p1 = attrs.get("password")
        p2 = attrs.pop("password2", None)
        if p1 != p2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # run Django password validators
        try:
            password_validation.validate_password(password=p1, user=User(**{k: attrs.get(k) for k in ("username", "email")}))
        except Exception as exc:
            raise serializers.ValidationError({"password": list(exc.messages) if hasattr(exc, "messages") else str(exc)})
        return attrs

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.password = make_password(pwd)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
