import React from 'react';
import { Link } from 'react-router-dom';

const Account = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Administrar Cuenta</h1>
          <Link 
            to="/dashboard" 
            className="py-2 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Volver al Dashboard
          </Link>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <p>Esta es la página de administración de la cuenta. Aquí se podrá actualizar el perfil y cambiar la contraseña.</p>
          {/* Aquí iría la lógica para el perfil y cambio de contraseña */}
        </div>
      </div>
    </div>
  );
};

export default Account;
