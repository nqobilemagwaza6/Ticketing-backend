from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .models import User
from .serializers import RegisterSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user - matches frontend expectations"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    errors = {}
    for field, error_list in serializer.errors.items():
        errors[field] = error_list[0] if error_list else "Invalid value"
    
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Authenticate a user by email and password and create a session."""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'message': 'Please provide both email and password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        login(request, user)
        
        role_lower = user.role.lower() if user.role else 'user'
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.first_name,
                'role': role_lower,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'message': 'Invalid email or password.'},
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

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Handle forgot password request - sends email with reset link
    """
    serializer = ForgotPasswordSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'message': 'Please provide a valid email address'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    email = serializer.validated_data['email']
    
    try:
        user = User.objects.get(email=email)
        
        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
        
        # Debug: Print the link to console
        print("="*50)
        print("RESET LINK GENERATED:")
        print(reset_link)
        print("UID:", uid)
        print("TOKEN:", token)
        print("="*50)
        
        # Send email
        subject = 'Password Reset Request'
        message = f"""
Hello {user.first_name or user.email},

You requested a password reset. Click the link below to reset your password:

{reset_link}

If you didn't request this, please ignore this email.

This link will expire in 24 hours.

Thanks,
Your Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        # For security, always return success even if email doesn't exist
        return Response({
            'message': 'If an account exists with this email, a reset link has been sent.'
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        # For security, don't reveal that email doesn't exist
        return Response({
            'message': 'If an account exists with this email, a reset link has been sent.'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Error in forgot_password: {str(e)}")
        return Response(
            {'message': 'Failed to send reset email. Please try again later.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Handle password reset with uid and token
    """
    serializer = ResetPasswordSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'detail': 'Invalid data provided', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    uid = serializer.validated_data['uid']
    token = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']
    
    try:
        # Decode uid
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        # Check token validity
        if not default_token_generator.check_token(user, token):
            return Response(
                {'detail': 'Invalid or expired reset link'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password has been reset successfully'
        }, status=status.HTTP_200_OK)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {'detail': 'Invalid reset link'},
            status=status.HTTP_400_BAD_REQUEST
        )