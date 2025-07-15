import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api'; // Importar la instancia de axios configurada

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  // El token se manejará a través de los interceptores de axios
  // No es necesario un estado local para él aquí.

  useEffect(() => {
    const validateToken = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Verificar el token obteniendo el perfil del usuario
          const { data } = await api.get('/auth/me/');
          setUser(data);
        } catch (error) {
          // Si el token es inválido o expiró, limpiar
          console.error("Error de validación de sesión", error);
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('user');
          setUser(null);
        }
      }
      setLoading(false);
    };

    validateToken();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const { data } = await api.post('/auth/login/', { email, password });
      
      // Almacenar tokens y datos del usuario
      localStorage.setItem('token', data.tokens.access);
      localStorage.setItem('refreshToken', data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      setUser(data.user);
      setLoading(false);
      return { success: true };
    } catch (error) {
      console.error("Error en el login:", error.response?.data);
      setLoading(false);
      return { success: false, error: error.response?.data?.detail || 'Error al iniciar sesión' };
    }
  };

  const register = async (name, email, password, confirm_password) => {
    setLoading(true);
    try {
      const { data } = await api.post('/auth/register/', { name, email, password, confirm_password });
      
      // Almacenar tokens y datos del usuario
      localStorage.setItem('token', data.tokens.access);
      localStorage.setItem('refreshToken', data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      setUser(data.user);
      setLoading(false);
      return { success: true };
    } catch (error) {
      console.error("Error en el registro:", error.response?.data);
      setLoading(false);
      return { success: false, error: error.response?.data || 'Error al registrar usuario' };
    }
  };

  const logout = () => {
    // Opcional: llamar a un endpoint de logout para invalidar el refresh token en el backend
    // api.post('/auth/logout/', { refresh: localStorage.getItem('refreshToken') });
    
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setUser(null);
    // No es necesario borrar el header de axios, el interceptor lo maneja
    window.location.href = '/login'; // Redirigir al login
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !loading && !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
