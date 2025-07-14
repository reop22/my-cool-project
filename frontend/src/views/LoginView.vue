<!-- ПУТЬ: frontend/src/views/LoginView.vue -->
<template>
  <div class="login-wrapper">
    <div class="login-container" v-auto-animate>
      <div class="text-center mb-5">
        <img src="/logo.svg" alt="Digital Dispatcher Logo" class="login-logo"/>
        <h1 class="login-title">Вход в систему</h1>
        <p class="login-subtitle">Digital Dispatcher</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="p-fluid">
        <div class="field mb-4">
          <label for="username">Имя пользователя</label>
          <InputText id="username" v-model="username" required size="large" />
        </div>
        <div class="field mb-4">
          <label for="password">Пароль</label>
          <Password 
            id="password" 
            v-model="password" 
            required 
            :feedback="false" 
            toggleMask 
            inputClass="p-inputtext-lg"
          />
        </div>
        
        <Button 
          type="submit" 
          :loading="loading" 
          class="w-full p-button-lg mt-5"
        >
          <i class="pi pi-arrow-right mr-2"></i>
          <span>Войти</span>
        </Button>
        
        <transition name="fade">
          <Message v-if="errorMessage" severity="error" :closable="false" class="mt-4">{{ errorMessage }}</Message>
        </transition>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Message from 'primevue/message';

const username = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');
const authStore = useAuthStore();

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = "Пожалуйста, заполните все поля.";
    return;
  }
  loading.value = true;
  errorMessage.value = '';
  try {
    await authStore.login(username.value, password.value);
  } catch (error) {
    errorMessage.value = 'Не удалось войти. Проверьте логин и пароль.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-wrapper { display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 1rem; background: var(--surface-ground); }
.login-container { width: 100%; max-width: 420px; padding: 2.5rem 3rem; background: var(--surface-a); border-radius: 12px; box-shadow: var(--shadow-md); }
.login-logo { height: 52px; margin-bottom: 1.5rem; }
.login-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
.login-subtitle { color: var(--text-secondary); margin-top: 0; font-size: 1.1rem; }
.field label { display: block; margin-bottom: 0.75rem; font-weight: 500; font-size: 0.9rem; }
</style>