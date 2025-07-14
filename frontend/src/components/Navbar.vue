<!-- ПУТЬ: frontend/src/components/Navbar.vue -->
<template>
  <nav class="navbar" v-if="authStore.isAuthenticated">
    <div class="navbar-container">
      <router-link to="/" class="navbar-brand">
        <img src="/logo.svg" alt="Logo" class="logo">
        <span>Digital Dispatcher</span>
      </router-link>
      <div class="navbar-user-info" v-if="authStore.user">
        <div class="user-details">
          <span class="user-name">{{ authStore.user.full_name || authStore.user.username }}</span>
          <span class="user-role"> ({{ authStore.userRoles.join(', ') }})</span>
        </div>
        <Button @click="authStore.logout()" label="Выйти" icon="pi pi-sign-out" severity="danger" text />
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import Button from 'primevue/button';
const authStore = useAuthStore();
</script>

<style scoped>
.navbar { background-color: var(--surface-a); border-bottom: 1px solid var(--surface-border); padding: 0 2rem; position: sticky; top: 0; z-index: 1020; box-shadow: var(--shadow-sm); }
.navbar-container { display: flex; justify-content: space-between; align-items: center; height: 64px; max-width: 1400px; margin: 0 auto; }
.navbar-brand { display: flex; align-items: center; gap: 0.75rem; font-size: 1.25rem; font-weight: 600; color: var(--text-primary); text-decoration: none; }
.logo { height: 32px; }
.navbar-user-info { display: flex; align-items: center; gap: 1rem; }
.user-details { text-align: right; }
.user-name { font-weight: 600; }
.user-role { color: var(--text-secondary); font-size: 0.9em; }
</style>