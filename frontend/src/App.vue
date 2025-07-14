<!-- ПУТЬ: frontend/src/App.vue -->
<template>
  <div id="app-wrapper">
    <Navbar v-if="authStore.isAuthenticated" />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <ConfirmDialog />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
import { useAuthStore } from './stores/auth';
import ConfirmDialog from 'primevue/confirmdialog';

const authStore = useAuthStore();
</script>

<style>
:root {
  --p-primary-color: #4F46E5;
  --p-primary-color-text: #FFFFFF;
  --color-primary-light: #e0e7ff;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-info: #3B82F6;
  --text-primary: #111827;
  --text-secondary: #4B5563;
  --text-muted: #6B7280;
  --surface-ground: #F9FAFB;
  --surface-a: #FFFFFF;
  --surface-border: #E5E7EB;
  --font-family: 'Inter', sans-serif;
  --border-radius: 8px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}

*, *::before, *::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: var(--font-family);
  background-color: var(--surface-ground);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.p-component {
  font-family: var(--font-family) !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.main-content {
  flex-grow: 1;
  padding: 2rem;
}
.container {
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}
</style>