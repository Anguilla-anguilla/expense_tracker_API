from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('api/', views.ExpenseAPIView.as_view(), name='api'),
    path('api/<int:expense_id', views.ExpenseDetailAPIVIew.as_view(), name='api-id'),
    path('api/list/', views.ExpenseViewSet.as_view({'get': 'list'}), name='api-set')
]
