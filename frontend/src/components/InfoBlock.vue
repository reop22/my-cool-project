<!-- ПУТЬ: frontend/src/components/InfoBlock.vue -->
<template>
  <div class="info-block">
    <div class="info-block-header">
      <i :class="icon"></i>
      <h3 class="info-block-title">{{ title }}</h3>
    </div>
    <div class="info-block-content" v-auto-animate>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>

defineProps({
  title: String,
  icon: String,
});
</script>

<style scoped>
.info-block { background-color: var(--surface-a); border: 1px solid var(--surface-border); border-radius: var(--border-radius); height: 100%; }
.info-block-header { display: flex; align-items: center; gap: 0.75rem; padding: 1rem 1.25rem; border-bottom: 1px solid var(--surface-border); }
.info-block-header i { font-size: 1.25rem; color: var(--p-primary-color); }
.info-block-title { font-size: 1.125rem; margin: 0; font-weight: 600; }
.info-block-content { padding: 1.25rem; }
.info-block-content p { margin: 0 0 0.75rem 0; line-height: 1.6; color: var(--text-secondary); }
.info-block-content p:last-child { margin-bottom: 0; }
.info-block-content strong { color: var(--text-primary); font-weight: 500; }
</style>