<!-- ПУТЬ: frontend/src/views/TripSheetList.vue -->
<template>
  <div class="list-container container">
    <PageHeader :title="title" :subtitle="subtitle" />
    <Card>
      <template #content>
        <TripSheetListSkeleton v-if="loading" />
        <div v-else-if="error" class="message-container error-message"><i class="pi pi-times-circle"></i><p><strong>Ошибка загрузки данных</strong></p><p>{{ error }}</p></div>
        <DataTable v-else :value="sheets" responsiveLayout="scroll" dataKey="id">
          <template #empty><div class="message-container no-data-message"><i class="pi pi-inbox"></i><p>Нет листов в данном статусе.</p></div></template>
          <Column field="sheet_number" header="Номер листа" :sortable="true"></Column>
          <Column field="creation_date" header="Дата создания" :sortable="true"><template #body="{ data }">{{ new Date(data.creation_date).toLocaleDateString() }}</template></Column>
          <Column field="driver.full_name" header="Водитель" :sortable="true"></Column>
          <Column header="Автомобиль"><template #body="{ data }">{{ data.car_model }} ({{ data.car_plate }})</template></Column>
          <Column header="Действие">
            <template #body="{ data }">
              <router-link :to="`/trip-sheets/${data.id}`">
                <Button :label="actionButtonLabel" icon="pi pi-folder-open" text />
              </router-link>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import apiClient from '../services/api';
import PageHeader from '../components/PageHeader.vue';
import Card from 'primevue/card';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import TripSheetListSkeleton from '../components/TripSheetListSkeleton.vue';

const route = useRoute();
const authStore = useAuthStore();
const sheets = ref([]);
const loading = ref(true);
const error = ref('');

// ИСПРАВЛЕНИЕ ЗДЕСЬ: Добавляем статус 'завершен'
const statusMap = { 
  'создан водителем': { title: 'Мои черновики', subtitle: 'Путевые листы, ожидающие отправки на согласование.'}, 
  'ожидает предрейсового медосмотра': { title: 'Ожидают медосмотра', subtitle: 'Список документов, ожидающих ваших действий.' }, 
  'ожидает предрейсового техосмотра': { title: 'Ожидают техосмотра', subtitle: 'Список документов, ожидающих ваших действий.' }, 
  'ожидает выпуска диспетчером': { title: 'Готовы к выдаче', subtitle: 'Список документов, ожидающих ваших действий.' }, 
  'в рейсе': { title: 'В рейсе', subtitle: 'Путевые листы, находящиеся в процессе выполнения.' }, 
  'ожидает послерейсового медосмотра': { title: 'Ожидают послерейсового осмотра', subtitle: 'Список документов, ожидающих ваших действий.' }, 
  'ожидает послерейсового техосмотра': { title: 'Ожидают послерейсового осмотра', subtitle: 'Список документов, ожидающих ваших действий.' }, 
  'ожидает отметки о возвращении диспетчером': { title: 'Ожидают закрытия смены', subtitle: 'Список документов, ожидающих ваших действий.' },
  'завершен': { title: 'На финальное утверждение', subtitle: 'Листы, ожидающие финального расчета и утверждения администратором.'},
  'готов к скачиванию': { title: 'Готовые к скачиванию', subtitle: 'Полностью оформленные путевые листы, доступные для скачивания.' }
};

const statusKey = computed(() => route.query.status);
const title = computed(() => statusMap[statusKey.value]?.title || 'Список путевых листов');
const subtitle = computed(() => statusMap[statusKey.value]?.subtitle || '');
const actionButtonLabel = computed(() => {
    if (statusKey.value === 'готов к скачиванию') return 'Проверить / Скачать';
    if (statusKey.value === 'завершен') return 'Утвердить';
    return 'Открыть / Обработать';
});

const fetchSheets = async (statusValue) => {
  if (!statusValue) {
      sheets.value = [];
      return;
  }
  loading.value = true;
  error.value = '';
  try {
    const response = await apiClient.get('/trip-sheets/', { params: { status: statusValue } });
    sheets.value = response.data;
  } catch (err) {
    const detail = err.response?.data?.detail;
    error.value = `Ошибка API: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`;
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchSheets(statusKey.value));
watch(statusKey, (newStatus) => fetchSheets(newStatus));
</script>

<style scoped>
.message-container { text-align: center; padding: 3rem; border: 1px dashed var(--surface-border); border-radius: var(--border-radius); color: var(--text-secondary); }
.message-container i { font-size: 3rem; margin-bottom: 1rem; display: block; }
.error-message { color: var(--color-danger); border-color: var(--color-danger); }
</style>