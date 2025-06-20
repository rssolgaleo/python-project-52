import django_filters
from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Status',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Executor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Label',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='Only my tasks',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
