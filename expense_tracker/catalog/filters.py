import django_filters
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='createdAt',
                                               lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='createdAt',
                                             lookup_expr='lte')
    class Meta:
        model = Expense
        fields = ['start_date', 'end_date']