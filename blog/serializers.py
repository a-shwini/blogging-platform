from rest_framework import serializers
from .models import Post, Category, SubscriptionPlan, Subscription

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()  # Serialize author name
    publication_date = serializers.DateTimeField(format="%Y-%m-%d")  # Serialize publication date

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'publication_date','image', 'category']  # Include required fields

    def get_author(self, obj):
        return obj.author.username

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'