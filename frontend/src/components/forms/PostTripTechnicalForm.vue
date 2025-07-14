<!-- ПУТЬ: frontend/src/components/forms/PostTripTechnicalForm.vue -->
<template>
  <Fieldset legend="Действие: Послерейсовый технический контроль" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12 md:col-6">
        <label for="odometer-end">Показания одометра при возвращении (км)</label>
        <InputNumber id="odometer-end" v-model="formData.arrival_odometer" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="fuel-end">Остаток горючего при возвращении (л)</label>
        <InputNumber id="fuel-end" v-model="formData.fuel_balance_end" required mode="decimal" :minFractionDigits="1" />
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-check" label="Автомобиль принят, передать диспетчеру" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from "vue-toastification";
import Fieldset from 'primevue/fieldset';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);
const formData = reactive({
  arrival_odometer: null,
  fuel_balance_end: null,
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/post-trip-technical`, formData);
    toast.success('Автомобиль успешно принят после рейса!');
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