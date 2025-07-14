<!-- ПУТЬ: frontend/src/components/TechnicalCheckForm.vue -->
<template>
  <Card class="form-section">
    <template #title>Предрейсовый технический контроль</template>
    <template #content>
      <form @submit.prevent="handleSubmit" class="p-fluid grid">
        <div class="p-field col-12 md:col-6">
          <label for="odometer-start">Показания одометра (км)</label>
          <InputNumber id="odometer-start" v-model="formData.odometer_start" required />
        </div>
        <div class="p-field col-12 md:col-6">
          <label for="fuel-start">Остаток горючего (л)</label>
          <InputNumber id="fuel-start" v-model="formData.fuel_remaining_start" required mode="decimal" :minFractionDigits="1" />
        </div>
        <div class="p-field col-12">
          <label for="mechanic-notes">Заметки механика</label>
          <Textarea id="mechanic-notes" v-model="formData.mechanic_check_notes" rows="3" autoResize />
        </div>
        <div class="col-12">
          <Button type="submit" :loading="loading" icon="pi pi-check" label="Автомобиль исправен, передать диспетчеру" />
        </div>
      </form>
    </template>
  </Card>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../services/api';
import { useToast } from "vue-toastification";
import Card from 'primevue/card';
import InputNumber from 'primevue/inputnumber';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const formData = reactive({
  odometer_start: null,
  fuel_remaining_start: null,
  mechanic_check_notes: 'Автомобиль технически исправен, выезд разрешен.'
});
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/technical`, formData);
    toast.success('Техосмотр успешно завершен!');
    emit('update-successful');
  } catch (err) {
    toast.error(`Ошибка сохранения: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-section { border-left: 5px solid var(--color-warning); }
.p-field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>