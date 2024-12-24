from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .filters import ExpenseFilter
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer


def get_or_create_category(category_name):
    try:
        return Category.objects.get(category=category_name)
    except Category.DoesNotExist:
        category_serializer = CategorySerializer(data={'category':
                                                        category_name})
        if category_serializer.is_valid():
            category = category_serializer.save()
        else:
            return None
    return category


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ExpenseFilter
    ordering_fields = ['createdAt']


class ExpenseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    @extend_schema(request=ExpenseSerializer)
    def post(self, request):
        category_name = request.data.get('category')
        category = get_or_create_category(category_name)
        if not category:
            return Response({'error': 'Invalid category'},
                            status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get('amount')) < 0:
            return Response({'error': 'Invalid amount'},
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


class ExpenseDetailAPIVIew(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    def get_expense(self, expence_id, user_id):
        try:
            return Expense.objects.get(id=expence_id, user=user_id)
        except Expense.DoesNotExist:
            return None

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
            if int(request.data.get('amount')) < 0:
                return Response({'error': 'Invalid amount'},
                                status=status.HTTP_400_BAD_REQUEST)
            data['amount'] = request.data.get('amount')
        if request.data.get('category'):
            category_name = request.data.get('category')
            category = get_or_create_category(category_name)
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