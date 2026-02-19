from rest_framework import serializers
from .models import Ticket
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    # Show full name of assigned user
    agent = serializers.SerializerMethodField(read_only=True)
    
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
