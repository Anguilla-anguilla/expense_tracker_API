import django_filters
from .models import Expense, Category


class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='createdAt',
                                               lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='createdAt',
                                             lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category_id__category',
                                          lookup_expr='iexact')
    
    class Meta:
        model = Expense
        fields = ['start_date', 'end_date', 'category']