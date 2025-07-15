from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Task.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id', 
            'owner', 
            'title', 
            'description', 
            'status', 
            'priority', 
            'due_date', 
            'created_at', 
            'updated_at'
        ]
