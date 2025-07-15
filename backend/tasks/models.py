from django.db import models
from django.conf import settings

class TaskStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    IN_PROGRESS = 'in_progress', 'En Progreso'
    COMPLETED = 'completed', 'Completada'
    CANCELLED = 'cancelled', 'Cancelada'

class TaskPriority(models.TextChoices):
    LOW = 'low', 'Baja'
    MEDIUM = 'medium', 'Media'
    HIGH = 'high', 'Alta'
    URGENT = 'urgent', 'Urgente'

class Task(models.Model):
    """
    Modelo de Tareas. Cada tarea está asociada a un usuario.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=TaskStatus.choices, 
        default=TaskStatus.PENDING
    )
    priority = models.CharField(
        max_length=20, 
        choices=TaskPriority.choices, 
        default=TaskPriority.MEDIUM
    )
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at'] # Ordenar por defecto por fecha de creación descendente
        
    def __str__(self):
        return self.title
