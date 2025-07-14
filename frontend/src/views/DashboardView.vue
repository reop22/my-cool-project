<!-- ПУТЬ: frontend/src/views/DashboardView.vue -->
<template>
  <div class="dashboard-container container">
    <PageHeader 
      title="Панель управления" 
      :subtitle="authStore.user ? `Добро пожаловать, ${authStore.user.full_name}!` : ''"
    />
    <div class="actions-grid" v-auto-animate>
      <!-- Карточка водителя -->
      <Card v-if="authStore.isDriver" class="interactive-card" style="--card-accent-color: var(--color-info)">
        <template #title><div class="card-title"><i class="pi pi-user card-icon"></i><span>Задачи водителя</span></div></template>
        <template #content>
          <div class="action-links">
            <router-link to="/trip-sheets/new"><Button label="Создать путевой лист" icon="pi pi-plus" text class="w-full text-left"/></router-link>
            <router-link to="/trip-sheets/list?status=создан водителем"><Button label="Черновики" icon="pi pi-file" text class="w-full text-left"/></router-link>
            <router-link to="/trip-sheets/list?status=в рейсе"><Button label="В рейсе" icon="pi pi-spin pi-cog" text class="w-full text-left"/></router-link>
          </div>
        </template>
      </Card>
      
      <!-- Карточка врача -->
      <Card v-if="authStore.isDoctor" class="interactive-card" style="--card-accent-color: var(--color-success)">
        <template #title><div class="card-title"><i class="pi pi-heart-fill card-icon"></i><span>Задачи врача</span></div></template>
        <template #content>
          <div class="action-links">
            <router-link to="/trip-sheets/list?status=ожидает предрейсового медосмотра">
              <Button label="Ожидают предрейсового осмотра" icon="pi pi-user-plus" text class="w-full text-left"/>
            </router-link>
            <router-link to="/trip-sheets/list?status=ожидает послерейсового медосмотра">
              <Button label="Ожидают послерейсового осмотра" icon="pi pi-user-minus" text class="w-full text-left"/>
            </router-link>
          </div>
        </template>
      </Card>
      
      <!-- Карточка механика -->
      <Card v-if="authStore.isMechanic" class="interactive-card" style="--card-accent-color: var(--color-warning)">
        <template #title><div class="card-title"><i class="pi pi-wrench card-icon"></i><span>Задачи механика</span></div></template>
        <template #content>
          <div class="action-links">
            <router-link to="/trip-sheets/list?status=ожидает предрейсового техосмотра"><Button label="Ожидают предрейсового осмотра" icon="pi pi-arrow-right-square" text class="w-full text-left"/></router-link>
            <router-link to="/trip-sheets/list?status=ожидает послерейсового техосмотра"><Button label="Ожидают послерейсового осмотра" icon="pi pi-arrow-left-square" text class="w-full text-left"/></router-link>
          </div>
        </template>
      </Card>
      
      <!-- Карточка диспетчера -->
      <Card v-if="authStore.isDispatcher" class="interactive-card" style="--card-accent-color: #8B5CF6">
        <template #title><div class="card-title"><i class="pi pi-send card-icon"></i><span>Задачи диспетчера</span></div></template>
        <template #content>
          <div class="action-links">
            <router-link to="/trip-sheets/list?status=ожидает выпуска диспетчером"><Button label="Готовы к выдаче" icon="pi pi-send" text class="w-full text-left"/></router-link>
            <router-link to="/trip-sheets/list?status=ожидает отметки о возвращении диспетчером"><Button label="Ожидают закрытия смены" icon="pi pi-flag-fill" text class="w-full text-left"/></router-link>
          </div>
        </template>
      </Card>
      
      <!-- Карточка администратора -->
      <Card v-if="authStore.isAdmin" class="interactive-card" style="--card-accent-color: var(--text-muted)">
        <template #title><div class="card-title"><i class="pi pi-shield card-icon"></i><span>Администрирование</span></div></template>
        <template #content>
          <div class="action-links">
            <router-link to="/users"><Button label="Управление пользователями" icon="pi pi-users" text class="w-full text-left"/></router-link>
            <router-link to="/admin/monitor"><Button label="Мониторинг всех листов" icon="pi pi-desktop" text class="w-full text-left"/></router-link>
            <router-link to="/trip-sheets/list?status=завершен">
              <Button label="На финальное утверждение" icon="pi pi-check-circle" severity="success" text class="w-full text-left"/>
            </router-link>
            <router-link to="/trip-sheets/list?status=готов к скачиванию">
              <Button label="Готовые к скачиванию" icon="pi pi-download" text class="w-full text-left"/>
            </router-link>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import Card from 'primevue/card';
import Button from 'primevue/button';
import PageHeader from '../components/PageHeader.vue';
const authStore = useAuthStore();
</script>

<style scoped>
.actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; }
.interactive-card { transition: transform 0.2s ease-out, box-shadow 0.2s ease-out; border-left: 5px solid var(--card-accent-color); }
.interactive-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-md); }
.card-title { display: flex; align-items: center; gap: 0.75rem; font-size: 1.25rem; }
.card-icon { font-size: 1rem; }
.action-links { display: flex; flex-direction: column; gap: 0.5rem; }
.p-button.p-button-text { color: var(--text-secondary); padding: 0.75rem; }
.p-button.p-button-text:hover { background-color: var(--color-primary-light) !important; color: var(--p-primary-color) !important; }
.text-left { text-align: left; justify-content: flex-start; }
</style>