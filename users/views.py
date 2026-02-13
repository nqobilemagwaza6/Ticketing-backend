from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import RegisterSerializer

# Function-based view to list all users
@api_view(['GET'])
def users_list(request):
    users = User.objects.all()
    serializer = RegisterSerializer(users, many=True)
    return Response(serializer.data)

# Function-based view to register a new user
@csrf_exempt
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)  # DRF parses JSON automatically
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)