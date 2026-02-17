from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth.password_validation import validate_password
from .serializers import UserSerializer

@api_view(['POST'])
def add_user(request):
    """
    Create a new user (Admin, Support, or User)
    """
    if not request.user.is_authenticated or request.user.role.lower() != 'admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    role = data.get('role', 'User')

    if not email or not password or not full_name or not role:
        return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=email, email=email, first_name=full_name, role=role.capitalize())
    user.set_password(password)

    # If role is Admin, make superuser
    if role.lower() == 'admin':
        user.is_superuser = True
        user.is_staff = True
    elif role.lower() == 'support':
        user.is_staff = True  # support can be staff but not superuser

    user.save()

    return Response({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'full_name': user.first_name,
            'role': user.role.lower(),
        }
    }, status=status.HTTP_201_CREATED)

from rest_framework.decorators import api_view

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    user_list = []
    for u in serializer.data:
        user_list.append({
            'id': u['id'],
            'email': u['email'],
            'full_name': u['first_name'],
            'role': u['role'].lower() if u['role'] else 'user',
            'active': u['is_active']
        })
    print("Fetched users:", user_list)

    return Response({
        'message': 'Users fetched successfully',
        'users': user_list
    }, status=200)
