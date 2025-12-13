from django.shortcuts import render
from rest_framework.response import Response # rest_framework is Django REST Framework, a powerful toolkit for 
# building Web APIs in Django.
# Response is used to return data from your API views to the client (like a browser or mobile app).
from rest_framework.decorators import api_view, permission_classes # api_view is a decorator provided by DRF.
# api_view is used to turn a Django view into an API view that can handle specific HTTP methods.
# Response is used to return data from your API views to the client (like a browser or mobile app).
# Response Works well with status codes and DRF features.
from rest_framework import  generics, filters, status # status is a module from DRF that provides HTTP status 
# codes in a readable format.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken # JWT (rest_framework_simplejwt) handles authentication tokens (refresh & access).
from .models import Task, Category
from .serializers import TaskSerializer, UserRegisterSerializer, UserProfileSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


 # request.data contains the data which sent by the user
    # data= mean the incoming data is sent by user valid it and save to the db.


# I created function-based views with DRF decorators:
def frontend(request):
    return render(request, 'list.html')

# class-based views (CBV) with DRF APIView / GenericAPIView

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all() # query_set is a class attribute in your view that tells DRF which objects this view will work with.
    # queryset → your model data
    serializer_class = UserRegisterSerializer # serializer_class → your serializer, lookup_field → which field to filter objects
    # serializer_class is a class attribute specifying which serializer the view uses.
    permission_classes = [AllowAny]

# loginUserView: APIView → handles POST manually, generates JWT tokens.
# uses APIView because JWT token generation is custom logic.
class loginUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request): # post() method in a DRF APIView is a Python function that handles HTTP POST requests.
                             # post → this method is called automatically whenever the client sends a POST request to this view.
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user) # generates refresh token for the logged-in user
            return Response({
                'refresh': str(refresh), # refresh token object
                'access': str(refresh.access_token) # automatically generates an access token
            })
        
        return Response({'error': 'Invalid credential'}, status=400)
# Response() → converts Python objects to JSON automatically using DRF renderers

# Permissions
# Most endpoints require authentication (IsAuthenticated) except login/register (AllowAny).


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserProfileSerializer(request.data)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user=request.user
    
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password changed successfully'})


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    serach_fields = ['title', 'description']  # Search Find all items where a field partially matches the search text.
    ordering_fields = ['created_at', 'title'] # Sort the list of items by a specified field (ascending or descending)
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
        # self.request → the current HTTP request object.
        # self.request.user → the currently logged-in user making the API request.
        # Your Task model probably has a "user=" field like this
        # user=self.request.user filters tasks so that only tasks belonging to the logged-in user are returned.
     
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user) 
       
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        return Category.objects.all()

class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    