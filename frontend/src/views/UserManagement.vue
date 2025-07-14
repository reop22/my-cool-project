<!-- ПУТЬ: frontend/src/views/UserManagement.vue -->
<template>
  <div class="user-management-container container">
    <PageHeader title="Управление пользователями" subtitle="Добавляйте, редактируйте и удаляйте пользователей системы." />
    
    <Card>
      <template #content>
        <DataTable :value="users" :loading="loading" responsiveLayout="scroll" paginator :rows="10" v-model:filters="filters" dataKey="id" :globalFilterFields="['username','full_name']">
          <template #header>
            <div class="table-header">
              <Button label="Добавить пользователя" icon="pi pi-plus" @click="openNewUserDialog" />
              <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global'].value" placeholder="Глобальный поиск" />
              </span>
            </div>
          </template>
          
          <template #empty>Пользователи не найдены.</template>
          <template #loading>Загрузка данных пользователей...</template>

          <Column field="id" header="ID" :sortable="true" style="min-width: 6rem"></Column>
          <Column field="full_name" header="Пользователь" :sortable="true" style="min-width: 14rem">
            <template #body="{ data }"><div>{{ data.full_name }}</div><small class="text-muted">{{ data.username }}</small></template>
          </Column>
          <Column header="Роли" style="min-width: 12rem">
            <template #body="{ data }"><div v-auto-animate><Tag v-for="role in data.roles" :key="role.id" :value="role.name" class="mr-2" :severity="getRoleSeverity(role.name)" /><span v-if="!data.roles.length" class="text-muted">Нет ролей</span></div></template>
          </Column>
          <Column header="Назначить роль" style="min-width: 20rem">
            <template #body="{ data }"><div class="role-assigner"><Dropdown v-model="selectedRoleId[data.id]" :options="availableRoles" optionLabel="name" optionValue="id" placeholder="Выберите роль" class="w-full" /><Button icon="pi pi-check" rounded severity="success" @click="confirmAssignRole(data.id, data.username)" :disabled="!selectedRoleId[data.id]"/></div></template>
          </Column>
           <Column header="Действия" bodyStyle="text-align:center; min-width: 8rem;">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" class="p-button-rounded p-button-text mr-2" @click="openEditUserDialog(data)" />
              <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" @click="confirmDeleteUser(data)" />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

    <!-- Модальное окно для создания/редактирования пользователя -->
    <Dialog v-model:visible="userDialogVisible" :style="{width: '450px'}" :header="dialogHeader" :modal="true" class="p-fluid">
      <div class="field">
        <label for="username">Имя пользователя (логин)</label>
        <InputText id="username" v-model.trim="editableUser.username" required="true" :disabled="editableUser.id" />
      </div>
       <div class="field">
        <label for="fullname">Полное имя (ФИО)</label>
        <InputText id="fullname" v-model.trim="editableUser.full_name" required="true" />
      </div>
       <div class="field">
        <label for="password">Пароль</label>
        <Password id="password" v-model="editableUser.password" :feedback="false" toggleMask :required="!editableUser.id" />
        <small v-if="editableUser.id">Оставьте поле пустым, чтобы не менять пароль.</small>
      </div>
      <template #footer>
        <Button label="Отмена" icon="pi pi-times" text @click="hideUserDialog"/>
        <Button :label="dialogMode === 'new' ? 'Создать' : 'Сохранить'" icon="pi pi-check" @click="saveUser" />
      </template>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../services/api';
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "vue-toastification";
import { FilterMatchMode } from 'primevue/api';
import PageHeader from '../components/PageHeader.vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Tag from 'primevue/tag';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Password from 'primevue/password';

const users = ref([]);
const availableRoles = ref([]);
const selectedRoleId = ref({});
const loading = ref(true);
const confirm = useConfirm();
const toast = useToast();
const filters = ref({'global': {value: null, matchMode: FilterMatchMode.CONTAINS}});

const userDialogVisible = ref(false);
const dialogMode = ref('new');
const dialogHeader = ref('');
const editableUser = ref({});

const openNewUserDialog = () => {
    editableUser.value = {};
    dialogMode.value = 'new';
    dialogHeader.value = 'Создать нового пользователя';
    userDialogVisible.value = true;
};

const openEditUserDialog = (user) => {
    editableUser.value = { ...user, password: '' };
    dialogMode.value = 'edit';
    dialogHeader.value = 'Редактировать пользователя';
    userDialogVisible.value = true;
};

const hideUserDialog = () => {
    userDialogVisible.value = false;
    editableUser.value = {};
};

const saveUser = async () => {
    if (dialogMode.value === 'new') {
        try {
            const response = await apiClient.post('/users/', editableUser.value);
            users.value.push(response.data);
            toast.success('Пользователь успешно создан!');
        } catch (err) {
            toast.error(`Ошибка создания: ${err.response?.data?.detail || err.message}`);
        }
    } else {
        try {
            const updatePayload = { ...editableUser.value };
            if (!updatePayload.password) {
                delete updatePayload.password;
            }
            const response = await apiClient.put(`/users/${editableUser.value.id}`, updatePayload);
            const index = users.value.findIndex(u => u.id === editableUser.value.id);
            if (index > -1) {
                users.value[index] = response.data;
            }
            toast.success('Пользователь успешно обновлен!');
        } catch (err) {
            toast.error(`Ошибка обновления: ${err.response?.data?.detail || err.message}`);
        }
    }
    hideUserDialog();
};

const confirmDeleteUser = (user) => {
    confirm.require({
        message: `Вы уверены, что хотите удалить пользователя '${user.username}'? Это действие необратимо.`,
        header: 'Подтверждение удаления',
        icon: 'pi pi-exclamation-triangle',
        acceptClass: 'p-button-danger',
        acceptLabel: 'Да, удалить',
        rejectLabel: 'Отмена',
        accept: () => deleteUser(user),
    });
};

const deleteUser = async (user) => {
    try {
        await apiClient.delete(`/users/${user.id}`);
        users.value = users.value.filter(u => u.id !== user.id);
        toast.success(`Пользователь '${user.username}' удален.`);
    } catch (err) {
        toast.error(`Ошибка удаления: ${err.response?.data?.detail || err.message}`);
    }
};

const fetchUsers = async () => {
  try {
    const response = await apiClient.get('/users/');
    users.value = response.data;
  } catch (err) {
    toast.error('Не удалось загрузить список пользователей.');
  }
};

const fetchRoles = async () => {
  try {
    const response = await apiClient.get('/roles/');
    availableRoles.value = response.data;
  } catch (err) {
    toast.error('Не удалось загрузить список ролей.');
  }
};

const confirmAssignRole = (userId, username) => {
    const roleId = selectedRoleId.value[userId];
    const roleName = availableRoles.value.find(r => r.id === roleId)?.name;
    confirm.require({
        message: `Вы уверены, что хотите назначить роль '${roleName}' пользователю '${username}'?`,
        header: 'Подтверждение действия',
        icon: 'pi pi-exclamation-triangle',
        acceptClass: 'p-button-success',
        accept: () => assignRoleToUser(userId)
    });
};

const assignRoleToUser = async (userId) => {
  const roleId = selectedRoleId.value[userId];
  try {
    const response = await apiClient.post(`/users/${userId}/assign-role?role_id=${roleId}`);
    const userIndex = users.value.findIndex(u => u.id === userId);
    if (userIndex !== -1) users.value[userIndex] = response.data;
    toast.success('Роль успешно назначена!');
    selectedRoleId.value[userId] = null;
  } catch (err) {
    toast.error(`Не удалось назначить роль: ${err.response?.data?.detail || err.message}`);
  }
};

const getRoleSeverity = (roleName) => {
    const severities = { 'администратор': 'danger', 'доктор': 'success', 'механик': 'warning', 'дежурный': 'info', 'водитель': 'primary' };
    return severities[roleName] || null;
};

onMounted(async () => {
  loading.value = true;
  await Promise.all([fetchUsers(), fetchRoles()]);
  loading.value = false;
});
</script>

<style scoped>
.table-header { display: flex; justify-content: space-between; align-items: center; }
.role-assigner { display: flex; align-items: center; gap: 0.5rem; }
.text-muted { color: var(--text-muted); }
.field { margin-bottom: 1rem; }
.field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>