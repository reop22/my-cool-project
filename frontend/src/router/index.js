// ПУТЬ: frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import DashboardView from '../views/DashboardView.vue';
import UserManagement from '../views/UserManagement.vue';
import TripSheetCreate from '../views/TripSheetCreate.vue';
import TripSheetList from '../views/TripSheetList.vue';
import TripSheetDetail from '../views/TripSheetDetail.vue';
import AdminMonitor from '../views/AdminMonitor.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginView, meta: { isPublic: true } },
  { path: '/', name: 'Dashboard', component: DashboardView },
  { path: '/users', name: 'UserManagement', component: UserManagement },
  { path: '/trip-sheets/new', name: 'TripSheetCreate', component: TripSheetCreate },
  { path: '/trip-sheets/list', name: 'TripSheetList', component: TripSheetList, props: (route) => ({ status: route.query.status }) },
  { path: '/trip-sheets/:id', name: 'TripSheetDetail', component: TripSheetDetail, props: true },
  { path: '/admin/monitor', name: 'AdminMonitor', component: AdminMonitor },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const hasToken = !!localStorage.getItem('access_token');
  
  if (to.meta.isPublic && hasToken) {
    return next({ name: 'Dashboard' });
  }

  if (!to.meta.isPublic && !hasToken) {
    return next({ name: 'Login' });
  }
  
  next();
});

export default router;