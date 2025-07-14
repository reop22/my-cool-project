<!-- ПУТЬ: frontend/src/components/DispatchForm.vue -->
<template>
  <Card class="form-section">
    <template #title>Выдача путевого листа</template>
    <template #content>
      <form @submit.prevent="handleSubmit" class="p-fluid">
        <div class="p-field mb-4">
          <label for="fuel-issued">Выдано горючего (л):</label>
          <InputNumber id="fuel-issued" v-model="formData.fuel_issued" required mode="decimal" :minFractionDigits="1" />
        </div>
        <Button type="submit" :loading="loading" icon="pi pi-send" label="Выпустить в рейс" />
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
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const formData = reactive({ fuel_issued: null });
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/dispatch`, formData);
    toast.success('Автомобиль выпущен в рейс!');
    emit('update-successful');
  } catch (err) {
    toast.error(`Ошибка выпуска: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-section { border-left: 5px solid var(--color-info); }
.p-field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>