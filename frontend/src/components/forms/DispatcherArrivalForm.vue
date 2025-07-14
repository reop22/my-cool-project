<!-- ПУТЬ: frontend/src/components/forms/DispatcherArrivalForm.vue -->
<template>
  <Fieldset legend="Действие: Отметка о возвращении и закрытие смены" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12">
        <label for="idle-details">Опоздания, ожидания, простои в пути, заезды в гараж и прочие отметки</label>
        <Textarea id="idle-details" v-model="formData.idle_time_details" rows="4" autoResize required />
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-check-square" label="Подтвердить возвращение и завершить путевой лист" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from "vue-toastification";
import Fieldset from 'primevue/fieldset';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);

// ИСПРАВЛЕНИЕ: Инициализируем поле, чтобы оно не было undefined
const formData = reactive({
  idle_time_details: 'Без опозданий и простоев.', // <-- Значение по умолчанию
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/dispatcher-arrival`, formData);
    toast.success('Путевой лист успешно завершен!');
    emit('update-successful');
  } catch (err) {
    let errorMessage = 'Ошибка сохранения.';
    if (err.response && err.response.data && err.response.data.detail) {
        if (typeof err.response.data.detail === 'string') {
            errorMessage = err.response.data.detail;
        } else {
            errorMessage = err.response.data.detail.map(e => `${e.loc.join(' -> ')}: ${e.msg}`).join('; ');
        }
    }
    toast.error(errorMessage);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
</style>