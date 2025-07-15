from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    ChangePasswordSerializer
)

User = get_user_model()

def get_tokens_for_user(user):
    """Genera tokens JWT para una instancia de usuario de Django."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        summary="Registra un nuevo usuario",
        responses={
            201: openapi.Response(
                description="Usuario registrado exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': UserSerializer,
                        'tokens': openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        summary="Autentica un usuario y devuelve tokens",
        responses={
            200: openapi.Response(
                description="Login exitoso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': UserSerializer,
                        'tokens': openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens
        }, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(summary="Obtiene o actualiza el perfil del usuario")
    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(summary="Cambia la contraseña del usuario")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)

# Manteniendo la vista de refresh por si se usa
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'refresh': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    summary="Refresca el token de acceso"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token_str = request.data.get('refresh')
        if not refresh_token_str:
            return Response({'error': 'Refresh token requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token_str)
        return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': f'Token inválido o expirado: {e}'}, status=status.HTTP_400_BAD_REQUEST)
