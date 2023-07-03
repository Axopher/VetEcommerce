import django_filters
from store.models import Order
from django_filters import DateFilter
from django import forms


class OrderFilter(django_filters.FilterSet):
    payment_start_date = DateFilter(field_name="date_ordered",
        lookup_expr='gte',
        label='From',
        widget=forms.DateInput(attrs={
            'placeholder': 'Select a start date',
            'type': 'date',
            'class':'form-control',
        })
    )
    payment_end_date = DateFilter(field_name="date_ordered",
        lookup_expr='lte',
        label='To',
        widget=forms.DateInput(attrs={
            'placeholder': 'Select an end date',
            'type': 'date',
            'class':'form-control',
        })
    )

    status = django_filters.ChoiceFilter(
        field_name="complete",
        label='Status',
        choices=(('True', 'True'), ('False', 'False')),
        empty_label='All',
        widget=forms.Select(attrs={
            'placeholder': 'Select status',
            'class': 'form-select',
        })
    )

    class Meta:
        model = Order
        fields = [ 'payment_start_date', 'payment_end_date','status']
