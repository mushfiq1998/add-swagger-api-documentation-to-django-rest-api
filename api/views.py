from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView

# For swagger
from rest_framework.generics import GenericAPIView

# For swagger APIView is replaced by GenericAPIView
# class StudentAPI(APIView):
class StudentAPI(GenericAPIView):

    # For swagger
    serializer_class = StudentSerializer

    # Retrive data from DB
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            # Get a single object from Studnet table 
            student = Student.objects.get(id=id)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        
        # Get query set (all model objects or rows) from Studnet table 
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        # Return query set to user in json
        return Response(serializer.data)
    
    # Create data in DB
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Send message with status code to user in json
            return Response({'msg': 'Data created'}, 
                            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                        status = status.HTTP_400_BAD_REQUEST)
    
    # Complete Data update
    def put(self, request, pk, format=None):
        id = pk
        student = Student.objects.get(pk=id)
        # perform compltete updation
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return response to user in json
            return Response({'msg': 'Complete Data updated'})
        return Response(serializer.errors, 
                        status = status.HTTP_400_BAD_REQUEST)
    
    # Partial Data update
    def patch(self, request, pk, format=None):
        id = pk
        student = Student.objects.get(pk=id)
        # perform compltete updation
        serializer = StudentSerializer(student, data=request.data, 
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return response to user in json
            return Response({'msg': 'Partial Data updated'})
        return Response(serializer.errors)
    
    # Data Delete from DB
    def delete(self, request, pk, format=None):
        id = pk
        student = Student.objects.get(pk=id)
        student.delete()
        # Return response to user in json
        return Response({'msg': 'Data Deleted'})
