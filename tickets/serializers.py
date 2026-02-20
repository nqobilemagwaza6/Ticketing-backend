from rest_framework import serializers
from .models import Ticket, Comment  # Import from current app (tickets)
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'ticket', 'user', 'user_email', 'user_full_name', 'text', 'created_at']
        read_only_fields = ['user', 'created_at', 'ticket']  # Make ticket read-only
    
    def get_user_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
        return None

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    # Show full name of assigned user
    agent = serializers.SerializerMethodField(read_only=True)
    filename = serializers.CharField(read_only=True)  # Add filename field
    
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='Support', is_active=True),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    def get_agent(self, obj):
        if obj.assigned_to:
            full_name = f"{obj.assigned_to.first_name or ''} {obj.assigned_to.last_name or ''}".strip()
            return full_name if full_name else obj.assigned_to.username
        return None

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assigned_to = validated_data.pop('assigned_to', None)
        if assigned_to:
            instance.assigned_to = assigned_to
            instance.status = 'In Progress'
        return super().update(instance, validated_data)