from django.urls import path
from task_manager.task_manager_app.statuses import views

urlpatterns = [
    path('', views.StatusListView.as_view(), name='status_list'),
    path('create/', views.StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
]
