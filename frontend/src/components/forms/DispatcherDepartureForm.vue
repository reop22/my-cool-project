<!-- ПУТЬ: frontend/src/components/forms/DispatcherDepartureForm.vue -->
<template>
  <Fieldset legend="Действие: Выдача задания и выпуск в рейс" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12">
        <label for="assignment-org">В распоряжение (наименование организации)</label>
        <InputText id="assignment-org" v-model="formData.assignment_organization_to" required />
      </div>
      <div class="field col-12">
        <label for="assignment-addr">Адрес подачи</label>
        <InputText id="assignment-addr" v-model="formData.assignment_address" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="departure-time">Время выезда по графику</label>
        <Calendar id="departure-time" v-model="formData.departure_scheduled_time" showTime hourFormat="24" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="arrival-time">Время возвращения по графику</label>
        <Calendar id="arrival-time" v-model="formData.arrival_scheduled_time" showTime hourFormat="24" required />
      </div>

      <Divider align="center" class="col-12">Движение горючего</Divider>
      
      <div class="field col-12 md:col-4">
        <label for="fuel-brand">Марка горючего</label>
        <InputText id="fuel-brand" v-model="formData.fuel_brand" required />
      </div>
      <div class="field col-12 md:col-4">
        <label for="fuel-code">Код</label>
        <InputText id="fuel-code" v-model="formData.fuel_code" />
      </div>
      <div class="field col-12 md:col-4">
        <label for="fuel-issued">Выдано, л</label>
        <InputNumber id="fuel-issued" v-model="formData.fuel_issued_liters" required mode="decimal" />
      </div>

      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-send" label="Выпустить автомобиль в рейс" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from "vue-toastification";
import Fieldset from 'primevue/fieldset';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import Calendar from 'primevue/calendar';
import Divider from 'primevue/divider';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);
const formData = reactive({
  assignment_organization_to: '',
  assignment_address: '',
  departure_scheduled_time: null,
  arrival_scheduled_time: null,
  fuel_brand: '',
  fuel_code: '',
  fuel_issued_liters: null,
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/dispatcher-departure`, formData);
    toast.success('Автомобиль успешно выпущен в рейс!');
    emit('update-successful');
  } catch (err) {
    toast.error(`Ошибка сохранения: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>