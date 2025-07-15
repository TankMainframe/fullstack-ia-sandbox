# Arquitectura del Sistema

Este documento describe la arquitectura general del proyecto, el stack tecnológico utilizado, los componentes principales y los flujos de comunicación.

## 1. Stack Tecnológico

El sistema se compone de un frontend moderno, un backend robusto y servicios externos para la autenticación.

- **Frontend:**
  - **Framework:** React.js
  - **Bundler:** Vite
  - **Estilos:** Tailwind CSS
  - **Enrutamiento:** React Router

- **Backend:**
  - **Framework:** Django
  - **API:** Django REST Framework (DRF)
  - **Base de Datos:** SQLite (para desarrollo)
  - **Autenticación JWT:** DRF Simple JWT

- **Servicios Externos:**
  - **Autenticación:** Firebase Authentication

## 2. Estructura del Proyecto

El repositorio está organizado en directorios separados para cada parte de la aplicación:

```
/
├── backend/         # Contiene el proyecto Django
│   ├── authentication/  # App de Django para autenticación
│   ├── tasks/         # App de Django para la gestión de tareas
│   └── backend_project/ # Configuración principal del proyecto Django
├── frontend/        # Contiene la aplicación React (Vite)
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   └── pages/
├── docs/            # Documentación del proyecto
└── firebase/        # Archivos de configuración de Firebase
```

## 3. Componentes Principales (Agentes)

- **Frontend:** Es una Single Page Application (SPA) responsable de toda la interfaz de usuario. Se comunica con el backend a través de una API REST para obtener y enviar datos. La autenticación inicial se delega a Firebase.

- **Backend:** Es una API RESTful que centraliza la lógica de negocio. Se encarga de validar los datos, interactuar con la base de datos y gestionar las sesiones de usuario a través de tokens JWT, después de una validación inicial con Firebase.

- **Firebase:** Actúa como el proveedor de identidad principal. Gestiona el registro de nuevos usuarios y la validación de credenciales, devolviendo un token de identidad que el backend utiliza para verificar la autenticidad del usuario.

## 4. Flujo de Autenticación

El flujo de comunicación entre los componentes para la autenticación es el siguiente:

1.  **Registro/Login de Usuario:**
    - El usuario introduce sus credenciales en la interfaz del **Frontend**.
    - El **Frontend** envía estas credenciales directamente a **Firebase Authentication**.
    - **Firebase** valida las credenciales, crea una nueva cuenta (o autentica una existente) y devuelve un *ID Token* al **Frontend**.

2.  **Autenticación con el Backend:**
    - El **Frontend** realiza una solicitud al endpoint `/api/auth/firebase-login/` del **Backend**, enviando el *ID Token* de Firebase.
    - El **Backend** recibe el token y utiliza el SDK de Firebase para verificar su validez.
    - Si el token es válido, el **Backend** busca un usuario local asociado a ese UID de Firebase. Si no existe, crea uno nuevo.
    - Finalmente, el **Backend** genera sus propios tokens (Access y Refresh) usando *Simple JWT* y los devuelve al **Frontend**.

3.  **Acceso a Rutas Protegidas:**
    - Para todas las solicitudes posteriores a endpoints protegidos (como la gestión de tareas), el **Frontend** adjunta el *Access Token* del backend en la cabecera `Authorization`.
    - El **Backend** utiliza *Simple JWT* para validar el token en cada solicitud y autorizar el acceso a los recursos.
