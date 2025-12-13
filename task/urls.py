
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.loginUserView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('change-password', views.change_password, name='change-password'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDeleteView.as_view(), name='task-detail-update-delete'),
    path('category/', views.CategoryListCreateView.as_view(), name='category'),
    path('category/<int:pk>/', views.CategoryRetrieveUpdateDeleteView.as_view(), name='category-update-delete'),
]

# .as_view() converts a class-based view into a callable view function that Django can use to handle HTTP requests. 
# It maps HTTP methods (GET, POST, etc.) to the class’s methods.