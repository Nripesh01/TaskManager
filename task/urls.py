
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.task_list),
    path('create/', views.task_create),
    path('<int:pk>/', views.task_detail),
    path('<int:pk>/update/', views.task_update),
    path('<int:pk>/delete/', views.task_delete),
    path('', views.frontend),
#     path('register/', views.RegisterUserView.as_view(), name='register'),
#     path('login/', views.loginUserView.as_view(), name='login'),
    
]