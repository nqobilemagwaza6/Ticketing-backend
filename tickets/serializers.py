from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'  # Include all fields
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']  # Make these fields immutable

    def create(self, validated_data):
        # We are not overriding it here since we handle user assignment in the view
        return super().create(validated_data)
