from rest_framework import serializers
from .models import Expense, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category',
                  'category_id', 'user', 'createdAt']