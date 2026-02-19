from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('current-user/', views.current_user, name='current-user'),
    path('users_list/', views.users_list, name='users-list'),
    # Password reset endpoints
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('admin_create_user/', views.admin_create_user, name='admin_create_user'),
    path('admin_update_user/<int:pk>/', views.admin_update_user, name='admin_update_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
]