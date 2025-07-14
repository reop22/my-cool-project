<!-- ПУТЬ: frontend/src/components/MedicalCheckForm.vue -->
<template>
  <Card class="form-section">
    <template #title>Предрейсовый медицинский осмотр</template>
    <template #content>
      <form @submit.prevent="handleSubmit" class="p-fluid">
        <div class="p-field mb-4">
          <label for="medical-notes">Заключение врача</label>
          <Textarea id="medical-notes" v-model="formData.medical_notes" required rows="4" autoResize />
        </div>
        <Button type="submit" :loading="loading" icon="pi pi-check" label="Подтвердить и передать механику" />
      </form>
    </template>
  </Card>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../services/api';
import { useToast } from "vue-toastification";
import Card from 'primevue/card';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true }});
const emit = defineEmits(['update-successful']);
const toast = useToast();
const formData = reactive({ medical_notes: 'Допущен к рейсу' });
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/medical`, formData);
    toast.success('Медосмотр успешно завершен!');
    emit('update-successful');
  } catch (err) {
    const errorMessage = err.response?.data?.detail || err.message;
    toast.error(`Ошибка сохранения: ${errorMessage}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-section { border-left: 5px solid var(--color-success); }
.p-field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>