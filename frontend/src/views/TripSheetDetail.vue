<!-- ПУТЬ: frontend/src/views/TripSheetDetail.vue -->
<template>
  <div class="detail-container container" v-auto-animate>
    <PageHeader :title="pageTitle" />
    <div v-if="loading" class="grid">
      <div class="col-12"><Skeleton height="4rem" class="mb-2" /></div>
      <div class="col-12"><Skeleton height="12rem" class="mb-4" /></div>
      <div class="col-12 md:col-6 lg:col-4"><Skeleton height="16rem" /></div>
      <div class="col-12 md:col-6 lg:col-4"><Skeleton height="16rem" /></div>
      <div class="col-12 md:col-6 lg:col-4"><Skeleton height="16rem" /></div>
    </div>
    <div v-else-if="error" class="message-container error-message">
      <i class="pi pi-exclamation-triangle"></i>
      <p><strong>Не удалось загрузить путевой лист</strong></p>
      <p>{{ error }}</p>
    </div>
    <div v-else-if="sheet">
      <header class="sheet-header">
        <Tag :value="sheet.status" :severity="getStatusSeverity(sheet.status)" />
        <Button v-if="canDownload" @click="downloadSheet" :loading="isDownloading" label="Скачать .docx" icon="pi pi-download"/>
      </header>
      
      <Message v-if="sheet.rejection_reason" severity="warn" :closable="false" class="mb-4">
        <strong>Лист возвращен на доработку.</strong> Причина: {{ sheet.rejection_reason }}
      </Message>

      <!-- ДИНАМИЧЕСКИЙ БЛОК ФОРМ -->
      <div class="actions-block mb-4">
        <DriverSubmitForm v-if="showDriverSubmitForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <PreTripMedicalForm v-if="showPreTripMedicalForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <PreTripTechnicalForm v-if="showPreTripTechnicalForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <DispatcherDepartureForm v-if="showDispatcherDepartureForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <DriverReturnForm v-if="showDriverReturnForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <PostTripMedicalForm v-if="showPostTripMedicalForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <PostTripTechnicalForm v-if="showPostTripTechnicalForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <DispatcherArrivalForm v-if="showDispatcherArrivalForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <AdminFinalizeForm v-if="showAdminFinalizeForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <PerformerReturnForm v-if="showPerformerReturnForm" :sheet-id="sheet.id" @update-successful="fetchSheet" />
        
        <Message v-if="sheet.status === 'готов к скачиванию'" severity="success">Этот путевой лист полностью оформлен и готов к скачиванию.</Message>
      </div>
      
      <div v-if="authStore.isAdmin" class="mb-4">
        <AdminReturnForm :sheet-id="sheet.id" @update-successful="fetchSheet" />
        <Button @click="confirmDelete" label="Удалить путевой лист" severity="danger" icon="pi pi-trash" class="mt-4" outlined />
      </div>

      <Accordion :multiple="true" :activeIndex="[0, 1, 2, 3]">
        <AccordionTab header="Основная информация (Шапка)">
            <div class="grid">
              <div class="col-12 md:col-6 lg:col-4"><InfoBlock title="Организация" icon="pi pi-building"><p><strong>Наименование:</strong> {{ sheet.organization_name || '—' }}</p><p><strong>Адрес:</strong> {{ sheet.organization_address || '—' }}</p><p><strong>Телефон:</strong> {{ sheet.organization_phone || '—' }}</p><p><strong>ОКПО:</strong> {{ sheet.organization_okpo || '—' }}</p></InfoBlock></div>
              <div class="col-12 md:col-6 lg:col-4"><InfoBlock title="Автомобиль" icon="pi pi-car"><p><strong>Марка, модель:</strong> {{ sheet.car_model || '—' }}</p><p><strong>Гос. номер:</strong> {{ sheet.car_plate || '—' }}</p><p><strong>Гаражный номер:</strong> {{ sheet.garage_number || '—' }}</p></InfoBlock></div>
              <div class="col-12 md:col-6 lg:col-4"><InfoBlock title="Водитель" icon="pi pi-user"><p><strong>ФИО:</strong> {{ sheet.driver?.full_name || '—' }}</p><p><strong>Табельный номер:</strong> {{ sheet.driver_personnel_number || '—' }}</p><p><strong>В/У:</strong> {{ sheet.driver_license_number || '—' }} ({{ sheet.driver_license_type || '—' }})</p><p><strong>Класс:</strong> {{ sheet.driver_class || '—' }}</p><p><strong>СНИЛС:</strong> {{ sheet.driver_snils || '—' }}</p></InfoBlock></div>
            </div>
        </AccordionTab>
        <AccordionTab header="Медицинский и технический контроль">
            <div class="grid">
              <div class="col-12 md:col-6"><InfoBlock title="Предрейсовый медосмотр" icon="pi pi-heart-fill"><p><strong>Время:</strong> {{ sheet.pre_trip_medical_check_time ? new Date(sheet.pre_trip_medical_check_time).toLocaleString() : 'Не проводился' }}</p><p><strong>Лицензия:</strong> {{ sheet.pre_trip_doctor_license || '—' }}</p><p><strong>Врач:</strong> {{ sheet.pre_trip_doctor?.full_name || '—' }}</p></InfoBlock></div>
              <div class="col-12 md:col-6"><InfoBlock title="Послерейсовый медосмотр" icon="pi pi-heart"><p><strong>Время:</strong> {{ sheet.post_trip_medical_check_time ? new Date(sheet.post_trip_medical_check_time).toLocaleString() : 'Не проводился' }}</p><p><strong>Лицензия:</strong> {{ sheet.post_trip_doctor_license || '—' }}</p><p><strong>Врач:</strong> {{ sheet.post_trip_doctor?.full_name || '—' }}</p></InfoBlock></div>
              <div class="col-12 md:col-6"><InfoBlock title="Предрейсовый техконтроль" icon="pi pi-wrench"><p><strong>Показания одометра:</strong> {{ sheet.departure_odometer || '—' }} км</p><p><strong>Заметка:</strong> {{ sheet.pre_trip_control_notes || '—' }}</p><p><strong>Механик:</strong> {{ sheet.departure_mechanic?.full_name || '—' }}</p></InfoBlock></div>
              <div class="col-12 md:col-6"><InfoBlock title="Послерейсовый техконтроль" icon="pi pi-wrench"><p><strong>Показания одометра:</strong> {{ sheet.arrival_odometer || '—' }} км</p><p><strong>Механик:</strong> {{ sheet.arrival_mechanic?.full_name || '—' }}</p></InfoBlock></div>
            </div>
        </AccordionTab>
        <AccordionTab header="Движение горючего">
            <div class="grid">
              <div class="col-12 md:col-6 lg:col-4"><InfoBlock title="Данные" icon="pi pi-database"><p><strong>Марка:</strong> {{ sheet.fuel_brand || '—' }}</p><p><strong>Код:</strong> {{ sheet.fuel_code || '—' }}</p><p><strong>Выдано:</strong> {{ sheet.fuel_issued_liters || '0' }} л</p></InfoBlock></div>
              <div class="col-12 md:col-6 lg:col-4"><InfoBlock title="Остатки" icon="pi pi-filter-slash"><p><strong>При выезде:</strong> {{ sheet.fuel_balance_start || '0' }} л</p><p><strong>При возвращении:</strong> {{ sheet.fuel_balance_end || '0' }} л</p></InfoBlock></div>
              <div class="col-12 md:col-6 lg:col-4"><InfoBlock title="Расход" icon="pi pi-chart-line"><p><strong>По норме:</strong> {{ sheet.fuel_consumption_norm || '0' }} л</p><p><strong>Фактический:</strong> {{ sheet.fuel_consumption_actual || '0' }} л</p><p><strong>Экономия/Перерасход:</strong> {{ (sheet.fuel_saving || -sheet.fuel_overconsumption) || '0' }} л</p></InfoBlock></div>
            </div>
        </AccordionTab>
        <AccordionTab header="Оборотная сторона (Выполнение задания)">
            <DataTable :value="sheet.route_points || []"><template #empty>Данные о маршруте не заполнены.</template><Column field="customer_number" header="Номер заказчика"></Column><Column field="departure_point" header="Отправление"></Column><Column field="arrival_point" header="Назначение"></Column><Column field="distance" header="Пробег, км"></Column></DataTable>
        </AccordionTab>
      </Accordion>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useToast } from 'vue-toastification';
import { useConfirm } from "primevue/useconfirm";
import { useRouter } from 'vue-router';
import apiClient from '../services/api';
import PageHeader from '../components/PageHeader.vue';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Skeleton from 'primevue/skeleton';
import Message from 'primevue/message';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InfoBlock from '../components/InfoBlock.vue';
import DriverSubmitForm from '../components/forms/DriverSubmitForm.vue';
import PreTripMedicalForm from '../components/forms/PreTripMedicalForm.vue';
import PostTripMedicalForm from '../components/forms/PostTripMedicalForm.vue';
import PreTripTechnicalForm from '../components/forms/PreTripTechnicalForm.vue';
import PostTripTechnicalForm from '../components/forms/PostTripTechnicalForm.vue';
import DispatcherDepartureForm from '../components/forms/DispatcherDepartureForm.vue';
import DispatcherArrivalForm from '../components/forms/DispatcherArrivalForm.vue';
import DriverReturnForm from '../components/forms/DriverReturnForm.vue';
import AdminFinalizeForm from '../components/forms/AdminFinalizeForm.vue';
import AdminReturnForm from '../components/forms/AdminReturnForm.vue';
import PerformerReturnForm from '../components/forms/PerformerReturnForm.vue';

const props = defineProps({ id: String });
const authStore = useAuthStore();
const toast = useToast();
const confirm = useConfirm();
const router = useRouter();
const sheet = ref(null);
const loading = ref(true);
const isDownloading = ref(false);
const error = ref('');

const pageTitle = computed(() => loading.value ? 'Загрузка...' : `Путевой лист № ${sheet.value?.sheet_number || ''}`);
const canDownload = computed(() => sheet.value && (authStore.isAdmin || sheet.value.status === 'готов к скачиванию'));

// --- COMPUTED СВОЙСТВА ДЛЯ ОТОБРАЖЕНИЯ ФОРМ ---
const showDriverSubmitForm = computed(() => sheet.value && ((authStore.user.id === sheet.value.driver?.id) || authStore.isAdmin) && sheet.value.status === 'создан водителем');
const showPreTripMedicalForm = computed(() => sheet.value && (authStore.isDoctor || authStore.isAdmin) && sheet.value.status === 'ожидает предрейсового медосмотра');
const showPreTripTechnicalForm = computed(() => sheet.value && (authStore.isMechanic || authStore.isAdmin) && sheet.value.status === 'ожидает предрейсового техосмотра');
const showDispatcherDepartureForm = computed(() => sheet.value && (authStore.isDispatcher || authStore.isAdmin) && sheet.value.status === 'ожидает выпуска диспетчером');
const showDriverReturnForm = computed(() => sheet.value && ((authStore.user.id === sheet.value.driver?.id) || authStore.isAdmin) && sheet.value.status === 'в рейсе');
const showPostTripMedicalForm = computed(() => sheet.value && (authStore.isDoctor || authStore.isAdmin) && sheet.value.status === 'ожидает послерейсового медосмотра');
const showPostTripTechnicalForm = computed(() => sheet.value && (authStore.isMechanic || authStore.isAdmin) && sheet.value.status === 'ожидает послерейсового техосмотра');
const showDispatcherArrivalForm = computed(() => sheet.value && (authStore.isDispatcher || authStore.isAdmin) && sheet.value.status === 'ожидает отметки о возвращении диспетчером');
const showAdminFinalizeForm = computed(() => sheet.value && authStore.isAdmin && sheet.value.status === 'завершен');
const showPerformerReturnForm = computed(() => {
  if (!sheet.value) return false;
  const isDoctorOnHisStage = authStore.isDoctor && sheet.value.status === 'ожидает предрейсового медосмотра';
  const isMechanicOnHisStage = authStore.isMechanic && sheet.value.status === 'ожидает предрейсового техосмотра';
  return isDoctorOnHisStage || isMechanicOnHisStage;
});

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
    'готов к скачиванию': 'success',
  }; 
  return severities[status] || 'secondary'; 
};

const fetchSheet = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await apiClient.get(`/trip-sheets/${props.id}`);
    sheet.value = response.data;
  } catch (err) {
    error.value = `Ошибка загрузки данных: ${err.response?.data?.detail || err.message}`;
    toast.error(error.value);
  } finally {
    loading.value = false;
  }
};

const downloadSheet = async () => {
  isDownloading.value = true;
  try {
    const response = await apiClient.get(`/trip-sheets/${props.id}/download`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `trip_sheet_${sheet.value.sheet_number}.docx`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    toast.success('Загрузка файла началась!');
  } catch (err) {
    toast.error('Не удалось скачать файл.');
  } finally {
    isDownloading.value = false;
  }
};

const confirmDelete = () => {
    confirm.require({
        message: 'Вы уверены, что хотите безвозвратно удалить этот путевой лист?',
        header: 'Подтверждение удаления',
        icon: 'pi pi-exclamation-triangle',
        acceptClass: 'p-button-danger',
        accept: () => deleteSheet(),
    });
};

const deleteSheet = async () => {
    try {
        await apiClient.delete(`/trip-sheets/${props.id}`);
        toast.success('Путевой лист успешно удален.');
        router.push('/');
    } catch (err) {
        toast.error(`Ошибка удаления: ${err.response?.data?.detail || err.message}`);
    }
};

onMounted(fetchSheet);
</script>

<style scoped>
.sheet-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.message-container { text-align: center; padding: 3rem; background-color: var(--surface-a); border-radius: var(--border-radius); border: 1px dashed var(--surface-border); color: var(--text-secondary); }
.message-container i { font-size: 3rem; margin-bottom: 1rem; display: block; }
.error-message { color: var(--color-danger); border-color: var(--color-danger); }
:deep(.p-accordion-header-link) { background-color: var(--surface-a); }
</style>