<!-- ПУТЬ: frontend/src/components/forms/DriverSubmitForm.vue -->
<template>
  <Fieldset legend="Действие Водителя: Отправка на согласование" :toggleable="true">
    <div class="form-container">
      <p>Вы заполнили первичные данные. Проверьте информацию и отправьте путевой лист на предрейсовый медицинский осмотр.</p>
      <Button 
        @click="handleSubmit" 
        :loading="loading" 
        label="Подтвердить и отправить врачу" 
        icon="pi pi-send" 
        severity="success"
      />
    </div>
  </Fieldset>
</template>

<script setup>
import { ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from 'vue-toastification';
import Fieldset from 'primevue/fieldset';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/submit-for-medical`);
    toast.success('Путевой лист успешно отправлен на медосмотр!');
    emit('update-successful');
  } catch (err) {
    toast.error(`Ошибка: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>