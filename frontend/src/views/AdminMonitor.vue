<!-- ПУТЬ: frontend/src/views/AdminMonitor.vue -->
<template>
  <div class="monitor-container container">
    <PageHeader title="Мониторинг путевых листов" subtitle="Просмотр всех документов в системе по статусам."/>
    <Card>
      <template #content>
        <TabView @tab-change="onTabChange" v-auto-animate>
          <TabPanel v-for="status in statuses" :key="status.key" :header="status.title">
            <TripSheetListSkeleton v-if="loading" />
            <div v-else-if="error" class="message-container error-message">
              <i class="pi pi-times-circle"></i>
              <p><strong>Ошибка загрузки</strong></p>
              <pre class="error-details">{{ error }}</pre>
            </div>
            <DataTable v-else :value="sheets" responsiveLayout="scroll" paginator :rows="10">
              <template #empty><div class="message-container no-data-message"><i class="pi pi-inbox"></i><p>Нет листов в данном статусе.</p></div></template>
              <Column field="sheet_number" header="Номер листа" :sortable="true"></Column>
              <Column field="status" header="Статус"><template #body="{data}"><Tag :value="data.status" :severity="getStatusSeverity(data.status)" /></template></Column>
              <Column field="driver.full_name" header="Водитель"></Column>
              <Column field="creation_date" header="Дата создания"><template #body="{data}">{{ new Date(data.creation_date).toLocaleString() }}</template></Column>
              <Column>
                <template #body="{data}">
                  <router-link :to="`/trip-sheets/${data.id}`">
                    <Button icon="pi pi-eye" text label="Просмотр"/>
                  </router-link>
                </template>
              </Column>
            </DataTable>
          </TabPanel>
        </TabView>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../services/api';
import PageHeader from '../components/PageHeader.vue';
import Card from 'primevue/card';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import TripSheetListSkeleton from '../components/TripSheetListSkeleton.vue';

// --- ИСПРАВЛЕНИЕ: Возвращаем apiValue, так как FastAPI ожидает именно его ---
const statuses = [ 
    { key: 'created_by_driver', title: 'Созданы', apiValue: 'создан водителем'}, 
    { key: 'awaiting_pre_trip_medical', title: 'На медосмотре (пред.)', apiValue: 'ожидает предрейсового медосмотра'}, 
    { key: 'awaiting_pre_trip_technical', title: 'На техосмотре (пред.)', apiValue: 'ожидает предрейсового техосмотра'},
    { key: 'awaiting_dispatcher_departure', title: 'У диспетчера (выезд)', apiValue: 'ожидает выпуска диспетчером'}, 
    { key: 'in_progress', title: 'В рейсе', apiValue: 'в рейсе'}, 
    { key: 'awaiting_post_trip_medical', title: 'На медосмотре (после)', apiValue: 'ожидает послерейсового медосмотра'},
    { key: 'awaiting_post_trip_technical', title: 'На техосмотре (после)', apiValue: 'ожидает послерейсового техосмотра'},
    { key: 'awaiting_dispatcher_arrival', title: 'У диспетчера (прием)', apiValue: 'ожидает отметки о возвращении диспетчером'},
    { key: 'completed', title: 'Завершены', apiValue: 'завершен'},
    { key: 'ready_for_download', title: 'Готовы к скачиванию', apiValue: 'готов к скачиванию'},
];

const sheets = ref([]);
const loading = ref(false);
const error = ref('');

const fetchSheets = async (statusValue) => {
  if (!statusValue) return;
  loading.value = true;
  error.value = '';
  try {
    // --- ИСПРАВЛЕНИЕ: Используем стандартный объект URLSearchParams для кодирования ---
    // Это самый надежный способ передавать параметры с кириллицей и пробелами
    const params = new URLSearchParams({ status: statusValue });
    const response = await apiClient.get(`/trip-sheets/?${params.toString()}`);
    sheets.value = response.data;
  } catch (err) {
    // Улучшаем отображение ошибки, чтобы видеть детали валидации
    if (err.response && err.response.data && err.response.data.detail) {
        error.value = JSON.stringify(err.response.data.detail, null, 2);
    } else {
        error.value = err.message || 'Неизвестная сетевая ошибка';
    }
  } finally {
    loading.value = false;
  }
};

const onTabChange = (event) => {
  const newStatusApiValue = statuses[event.index].apiValue;
  fetchSheets(newStatusApiValue);
};

const getStatusSeverity = (status) => {
    const severities = { 
        'создан водителем': 'contrast',
        'ожидает предрейсового медосмотра': 'info', 
        'ожидает предрейсового техосмотра': 'warning', 
        'ожидает выпуска диспетчером': 'primary', 
        'в рейсе': 'success',
        'ожидает послерейсового медосмотра': 'info',
        'ожидает послерейсового техосмотра': 'warning',
        'ожидает отметки о возвращении диспетчером': 'primary',
        'завершен': 'secondary',
        'готов к скачиванию': 'success'
    };
    return severities[status] || 'secondary';
};

// Загружаем данные для первой вкладки при монтировании компонента
onMounted(() => {
  fetchSheets(statuses[0].apiValue);
});
</script>

<style scoped>
.message-container { text-align: center; padding: 3rem; border-radius: var(--border-radius); color: var(--text-secondary); }
.message-container i { font-size: 3rem; margin-bottom: 1rem; display: block; }
.error-message { color: var(--color-danger); }
.error-details {
  max-width: 600px;
  margin: 1rem auto;
  padding: 1rem;
  background-color: #fff5f5;
  border-radius: 6px;
  text-align: left;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 0.85rem;
}
</style>