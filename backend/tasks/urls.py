from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Crear un router y registrar nuestro viewset con él.
router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

# Las URLs de la API son ahora determinadas automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]
