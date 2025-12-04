
from django.urls import path
from task import views

urlpatterns = [
    path('', views.task_list),
    path('create/', views.task_create),
    path('<int:pk>/', views.task_detail),
    path('<int:pk>/update/', views.task_update),
    path('<int:pk>/delete/', views.task_delete),
    path('frontend/', views.frontend),
]
    