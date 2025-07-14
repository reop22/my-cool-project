<!-- ПУТЬ: frontend/src/components/PageHeader.vue -->
<template>
  <header class="page-header">
    <Button 
      v-if="showBack" 
      icon="pi pi-arrow-left" 
      @click="goBack" 
      text 
      rounded 
      aria-label="Назад"
      class="back-button"
    />
    <div class="header-content">
      <h1 class="page-title">{{ title }}</h1>
      <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import Button from 'primevue/button';

defineProps({
  title: { type: String, required: true },
  subtitle: String,
});

const router = useRouter();
const route = useRoute();
const showBack = computed(() => route.path !== '/');
const goBack = () => router.back();
</script>

<style scoped>
.page-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; }
.page-title { font-size: 2.25rem; font-weight: 700; letter-spacing: -0.02em; margin: 0; }
.page-subtitle { margin-top: 0.5rem; font-size: 1.125rem; color: var(--text-secondary); margin-bottom: 0; }
.back-button { height: 48px; width: 48px; }
</style>