from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from datetime import datetime

from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer


class ExpenseListView:
    pass


class ExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    @extend_schema(request=ExpenseSerializer)
    def post(self, request):
        expense_detail_view = ExpenseDetailAPIVIew()
        
        category_name = request.data.get('category')
        category = expense_detail_view.check_category(category_name)
        if not category:
            return Response({'error': 'Invalid category'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'description': request.data.get('description'),
            'amount': request.data.get('amount'),
            'category_id': category.id,
            'createdAt': datetime.now().strftime('%Y-%m-%d'),
            'user_id': request.user.id
        }

        serializer = ExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailAPIVIew(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    def get_expense(self, expence_id, user_id):
        try:
            return Expense.objects.get(id=expence_id, user=user_id)
        except Expense.DoesNotExist:
            return None

    def get_category(self, category_name):
        try:
            return Category.objects.get(category=category_name)
        except Category.DoesNotExist:
            return None
        
    def check_category(self, category_name):
        category = self.get_category(category_name)
        if not category:
            category_serializer = CategorySerializer(data={'category':
                                                            category_name})
            if category_serializer.is_valid():
                category = category_serializer.save()
            else:
                return None
        return category

    def get(self, request, expense_id):
        expense_instance = self.get_expense(expense_id, request.user.id)
        if not expense_instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        expense_serializer = ExpenseSerializer(instance=expense_instance)
        return Response(expense_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ExpenseSerializer)
    def put(self, request, expense_id):
        expense_instance = self.get_expense(expense_id, request.user.id)
        if not expense_instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {'user': request.user.id}                 
        if request.data.get('description'):
            data['description'] = request.data.get('description')
        if request.data.get('amount'):
            data['amount'] = request.data.get('amount')
        if request.data.get('category'):
            category_name = request.data.get('category')
            category = self.check_category(category_name)
            data['category'] = category

        expense_serializer = ExpenseSerializer(instance=expense_instance,
                                               data=data,
                                               partial=True,
                                               context={'request': request})
        
        if expense_serializer.is_valid():
            expense_serializer.save()
            return Response(expense_serializer.data, status=status.HTTP_200_OK)
        
        return Response(expense_serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, expense_id):
        expense_instance = self.get_expense(expense_id, request.user.id)
        if not expense_instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        expense_instance.delete()
        return Response(status=status.HTTP_200_OK)