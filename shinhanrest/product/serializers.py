from rest_framework import serializers
from .models import Product, Comment

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        print(attrs)
        return attrs

    class Meta:
        model=Comment
        fields="__all__"