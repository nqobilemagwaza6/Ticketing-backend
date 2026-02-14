from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import RegisterSerializer, UserSerializer

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    """Register a new user - matches frontend expectations"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    # Provide more detailed error messages
    errors = {}
    for field, error_list in serializer.errors.items():
        errors[field] = error_list[0] if error_list else "Invalid value"
    
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    """Authenticate a user by email and password and create a session.
    
    This matches the frontend expectations:
    - Uses session authentication (not tokens)
    - Returns user object with role field
    - Frontend sends credentials: 'include' to handle cookies
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'message': 'Please provide both email and password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate using email as username
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        # Create session (this is what frontend expects with credentials: 'include')
        login(request, user)
        
        # Return user data in the format frontend expects
        # Make sure role is lowercase for frontend comparison
        role_lower = user.role.lower() if user.role else 'user'
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.first_name,  # frontend uses this field
                'role': role_lower,  # frontend checks role for redirect (expects 'admin' or 'user')
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'message': 'Invalid email or password.'},  # Match frontend error message
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
def logout_user(request):
    """Log out the current user"""
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def current_user(request):
    """Get the currently authenticated user"""
    if request.user.is_authenticated:
        role_lower = request.user.role.lower() if request.user.role else 'user'
        return Response({
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'full_name': request.user.first_name,
                'role': role_lower,
            }
        })
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def users_list(request):
    """List all users (for admin purposes)"""
    if not request.user.is_authenticated or request.user.role != 'Admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)