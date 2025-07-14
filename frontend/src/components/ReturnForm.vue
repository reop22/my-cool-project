<!-- ПУТЬ: frontend/src/components/ReturnForm.vue -->
<template>
  <Card class="form-section">
    <template #title>Завершение рейса</template>
    <template #content>
      <form @submit.prevent="handleSubmit" class="p-fluid grid">
        <div class="p-field col-12 md:col-6">
          <label for="odometer-end">Одометр при возвращении (км)</label>
          <InputNumber id="odometer-end" v-model="formData.odometer_end" required />
        </div>
        <div class="p-field col-12 md:col-6">
          <label for="fuel-end">Остаток горючего (л)</label>
          <InputNumber id="fuel-end" v-model="formData.fuel_remaining_end" required mode="decimal" :minFractionDigits="1" />
        </div>
        <div class="p-field col-12">
          <label for="trip-details">Отчет о маршруте (оборотная сторона)</label>
          <Textarea id="trip-details" v-model="formData.trip_points_details" rows="5" autoResize placeholder="Место отправления, назначения, время, пробег..."/>
        </div>
        <div class="col-12">
          <Button type="submit" :loading="loading" icon="pi pi-flag-fill" label="Завершить рейс" />
        </div>
      </form>
    </template>
  </Card>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../services/api';
import { useToast } from 'vue-toastification';
import Card from 'primevue/card';
import InputNumber from 'primevue/inputnumber';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const formData = reactive({
  odometer_end: null,
  fuel_remaining_end: null,
  trip_points_details: ''
});
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/return`, formData);
    toast.success('Рейс успешно завершен!');
    emit('update-successful');
  } catch (err) {
    toast.error(`Ошибка завершения: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-section { border-left: 5px solid var(--p-primary-color); }
.p-field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>