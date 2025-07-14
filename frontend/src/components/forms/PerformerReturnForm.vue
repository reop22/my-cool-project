<!-- ПУТЬ: frontend/src/components/forms/PerformerReturnForm.vue -->
<template>
  <Fieldset legend="Действие: Отклонить и вернуть водителю" :toggleable="true" class="border-danger mt-4">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12">
        <label for="rejection-reason">Причина отклонения (будет видна водителю)</label>
        <Textarea id="rejection-reason" v-model="formData.rejection_reason" rows="3" required autoResize placeholder="Например: неверно указан гос. номер, требуется уточнение данных и т.д."/>
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-times" label="Отклонить и вернуть" severity="danger" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from 'vue-toastification';
import Fieldset from 'primevue/fieldset';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({
  sheetId: { type: Number, required: true }
});
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);

const formData = reactive({
  rejection_reason: ''
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/return-by-performer`, formData);
    // --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
    toast.warning('Путевой лист отклонен и возвращен водителю на доработку!');
    emit('update-successful');
  } catch (err) {
    toast.error(`Ошибка: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.field label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.border-danger {
  border-left: 5px solid var(--color-danger);
}
</style>