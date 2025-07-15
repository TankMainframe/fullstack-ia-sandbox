from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Task, TaskStatus
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ver y editar tareas.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    # Habilitar filtrado por campos específicos
    filterset_fields = ['status', 'priority']
    # Habilitar búsqueda
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        Este viewset solo debe devolver las tareas
        del usuario actualmente autenticado.
        """
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Asigna el usuario actual como propietario de la tarea al crearla.
        """
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Devuelve estadísticas de las tareas para el usuario actual.
        """
        queryset = self.get_queryset()
        
        total_tasks = queryset.count()
        
        status_counts = queryset.values('status').annotate(count=Count('status'))
        
        stats_data = {status['status']: status['count'] for status in status_counts}
        
        # Asegurar que todos los estados estén presentes
        response_data = {
            'total_tasks': total_tasks,
            'pending_tasks': stats_data.get(TaskStatus.PENDING, 0),
            'in_progress_tasks': stats_data.get(TaskStatus.IN_PROGRESS, 0),
            'completed_tasks': stats_data.get(TaskStatus.COMPLETED, 0),
            'cancelled_tasks': stats_data.get(TaskStatus.CANCELLED, 0),
        }
        
        return Response(response_data)
