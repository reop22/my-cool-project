// ПУТЬ: frontend/src/stores/auth.js
import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null);
  const user = ref(JSON.parse(localStorage.getItem('user')) || null);

  const isAuthenticated = computed(() => !!token.value);
  const userRoles = computed(() => user.value?.roles.map(role => role.name) || []);
  const isAdmin = computed(() => userRoles.value.includes('администратор'));
  const isDriver = computed(() => userRoles.value.includes('водитель'));
  const isDoctor = computed(() => userRoles.value.includes('доктор'));
  const isMechanic = computed(() => userRoles.value.includes('механик'));
  const isDispatcher = computed(() => userRoles.value.includes('дежурный'));

  async function fetchUser() {
    if (token.value) {
      try {
        const response = await apiClient.get('/users/me');
        user.value = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (error) {
        console.error('Не удалось получить данные пользователя:', error);
        logout();
      }
    }
  }

  async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await apiClient.post('/login/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
      
    token.value = response.data.access_token;
    localStorage.setItem('access_token', token.value);
    
    await fetchUser();
    
    // Этот способ редиректа - самый надежный
    window.location.href = '/';
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  return { 
    token, user, login, logout, fetchUser,
    isAuthenticated, userRoles, isAdmin, isDriver, isDoctor, isMechanic, isDispatcher
  };
});