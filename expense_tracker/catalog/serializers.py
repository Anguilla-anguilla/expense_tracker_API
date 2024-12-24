from rest_framework import serializers
from .models import Expense, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'category',
                  'category_id', 'createdAt', 'user_id']

    def get_category(self, obj):
        if obj.category_id:
            return obj.category_id.category
        return None