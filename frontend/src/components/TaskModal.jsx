import React, { useState } from 'react';

const TaskModal = ({ isOpen, onClose, onSave, task }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  // Añadir más estados para otros campos como prioridad, estado, etc.

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ title, description });
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3 text-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900">{task ? 'Editar Tarea' : 'Crear Tarea'}</h3>
          <form onSubmit={handleSubmit} className="mt-2 px-7 py-3">
            <input
              type="text"
              placeholder="Título"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="mb-3 px-3 py-2 text-gray-700 bg-white border rounded-md w-full"
              required
            />
            <textarea
              placeholder="Descripción"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="mb-3 px-3 py-2 text-gray-700 bg-white border rounded-md w-full"
            />
            <div className="items-center px-4 py-3">
              <button
                type="submit"
                className="px-4 py-2 bg-indigo-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              >
                Guardar
              </button>
            </div>
          </form>
          <div className="items-center px-4 py-3">
            <button onClick={onClose} className="px-4 py-2 bg-gray-200 text-gray-800 text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-300">
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskModal;
