from django.shortcuts import render
from rest_framework.response import Response # rest_framework is Django REST Framework, a powerful toolkit for 
# building Web APIs in Django.
# Response is used to return data from your API views to the client (like a browser or mobile app).
from rest_framework.decorators import api_view # api_view is a decorator provided by DRF.
# api_view is used to turn a Django view into an API view that can handle specific HTTP methods.
# Response is used to return data from your API views to the client (like a browser or mobile app).
# Response Works well with status codes and DRF features.
from rest_framework import status # status is a module from DRF that provides HTTP status codes in a readable format.

from .models import Task
from .serializers import TaskSerializer

 # request.data contains the data which sent by the user
    # data= mean the incoming data is sent by user valid it and save to the db.

def frontend(request):
    return render(request, 'list.html')


@api_view(['GET'])
def task_list(request):
    task = Task.objects.all()
    serializer = TaskSerializer(task, many=True) # many=True It tells the serializer that you are  
# serializing a queryset (multiple objects), not just a single object.
    return Response(serializer.data)

@api_view(['POST'])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)

@api_view(['GET'])
def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['PUT'])
def task_update(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data) 
    # instance This is the existing object I want to update.”
    # data=request.data contains new data coming from the client in the POST/PUT/PATCH request.
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response({"message": "delete"})