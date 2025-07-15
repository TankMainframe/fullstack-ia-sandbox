import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import TaskModal from '../components/TaskModal';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/tasks/');
      const tasksData = response.data.results || response.data;
      setTasks(tasksData);
    } catch (err) {
      setError('Error al cargar las tareas.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateClick = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEditClick = (task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (taskId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
      try {
        await api.delete(`/tasks/${taskId}/`);
        fetchTasks(); // Recargar tareas
      } catch (err) {
        console.error("Error al eliminar la tarea:", err);
        setError("No se pudo eliminar la tarea.");
      }
    }
  };

  const handleSaveTask = async (taskData) => {
    try {
      if (editingTask) {
        // Actualizar tarea existente
        await api.put(`/tasks/${editingTask.id}/`, taskData);
      } else {
        // Crear nueva tarea
        await api.post('/tasks/', taskData);
      }
      setIsModalOpen(false);
      setEditingTask(null);
      fetchTasks(); // Recargar tareas
    } catch (err) {
      console.error("Error al guardar la tarea:", err);
      setError("No se pudo guardar la tarea.");
    }
  };

  const renderContent = () => {
    if (loading) return <p className="text-center text-gray-500">Cargando tareas...</p>;
    if (error) return <p className="text-center text-red-500">{error}</p>;
    if (tasks.length === 0) return <p className="text-center text-gray-500">No tienes tareas. ¡Crea una nueva!</p>;

    return (
      <ul className="space-y-4">
        {tasks.map((task) => (
          <li key={task.id} className="bg-white p-4 rounded-lg shadow flex justify-between items-center flex-wrap gap-2">
            <div className="flex-grow">
              <h3 className="font-bold text-lg">{task.title}</h3>
              <p className="text-sm text-gray-600">{task.description}</p>
              <div className="flex space-x-4 mt-2 text-xs">
                <span className="font-semibold capitalize">Prioridad: {task.priority}</span>
                <span className="font-semibold capitalize">Estado: {task.status}</span>
              </div>
            </div>
            <div className="flex space-x-2">
              <button onClick={() => handleEditClick(task)} className="text-blue-500 hover:text-blue-700 font-medium">Editar</button>
              <button onClick={() => handleDeleteClick(task.id)} className="text-red-500 hover:text-red-700 font-medium">Eliminar</button>
            </div>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
          <h1 className="text-3xl font-bold text-gray-900">Mis Tareas</h1>
          <div className="flex items-center space-x-4">
            <button 
              onClick={handleCreateClick}
              className="py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Crear Tarea
            </button>
            <Link 
              to="/dashboard" 
              className="py-2 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Volver al Dashboard
            </Link>
          </div>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          {renderContent()}
        </div>
      </div>
      <TaskModal 
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        onSave={handleSaveTask}
        task={editingTask}
      />
    </div>
  );
};

export default Tasks;
