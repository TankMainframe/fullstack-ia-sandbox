from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Añade campos adicionales si es necesario en el futuro.
    """
    # AbstractUser ya incluye: username, first_name, last_name, email, password,
    # groups, user_permissions, is_staff, is_active, is_superuser, last_login, date_joined.
    
    # Ejemplo de campo adicional:
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username
