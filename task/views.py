from django.shortcuts import render
from rest_framework.response import Response # rest_framework is Django REST Framework, a powerful toolkit for 
# building Web APIs in Django.
# Response is used to return data from your API views to the client (like a browser or mobile app).
from rest_framework.decorators import api_view, permission_classes # api_view is a decorator provided by DRF.
# api_view is used to turn a Django view into an API view that can handle specific HTTP methods.
# Response is used to return data from your API views to the client (like a browser or mobile app).
# Response Works well with status codes and DRF features.
from rest_framework import status, generics # status is a module from DRF that provides HTTP status 
# codes in a readable format.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken # JWT (rest_framework_simplejwt) handles authentication tokens (refresh & access).
from .models import Task
from .serializers import TaskSerializer, UserRegisterSerializer
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
    serializer_class = UserRegisterSerializer
    # serializer_class is a class attribute specifying which serializer the view uses.
    permission_classes = [AllowAny]

# loginUserView: APIView → handles POST manually, generates JWT tokens.
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
def task_list(request):
    task = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(task, many=True) # many=True It tells the serializer that you are  
# serializing a queryset (multiple objects), not just a single object.
    return Response(serializer.data)

# function-based views (FBV) with @api_view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # At this point, the DRF view has Python data, not JSON yet.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors) # Response is a special class used to send data back to the 
                                       # client (like Postman, a frontend app, or a mobile app)
    
    # The Response class uses renderers (by default, JSONRenderer) to convert Python objects to JSON.

    # If the request comes from a browser, DRF automatically uses the Browsable API renderer.

    # The browser will show a nice interactive page instead of raw JSON.

    # If the request comes from Postman, curl, or a mobile app, DRF sends raw JSON.
    
    # It automatically handles JSON serialization, so you don’t have to manually convert Python objects to JSON.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def task_update(request, pk):
    task = Task.objects.get(id=pk, user=request.user) # Fetch only tasks that belong to the logged-in user (security).
    serializer = TaskSerializer(instance=task, data=request.data) 
    # instance This is the existing object I want to update.”
    # data=request.data contains new data coming from the client in the POST/PUT/PATCH request.
    if serializer.is_valid():
        serializer.save(user=request.user) # user=request.user Make sure the user field stays linked to the logged-in user when saving changes.
        return Response(serializer.data) 
    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_delete(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return Response({"message": "delete successfully"})

