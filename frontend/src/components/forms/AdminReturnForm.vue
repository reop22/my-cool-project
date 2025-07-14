<!-- ПУТЬ: frontend/src/components/forms/AdminReturnForm.vue -->
<template>
  <Fieldset legend="Действие Администратора: Вернуть на доработку" :toggleable="true" class="border-danger">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12 md:col-6">
        <label for="target-status">Вернуть на этап</label>
        <Dropdown 
          id="target-status" 
          v-model="formData.target_status" 
          :options="statuses" 
          placeholder="Выберите этап" 
          required 
        />
      </div>
      <div class="field col-12">
        <label for="rejection-reason">Причина возврата (будет видна исполнителю)</label>
        <Textarea id="rejection-reason" v-model="formData.rejection_reason" rows="3" required autoResize />
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-undo" label="Вернуть на доработку" severity="danger" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from 'vue-toastification';
import Fieldset from 'primevue/fieldset';
import Dropdown from 'primevue/dropdown';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);

const formData = reactive({
  target_status: null,
  rejection_reason: ''
});

// Статусы, на которые можно вернуть лист
const statuses = ref([
    'создан водителем',
    'ожидает предрейсового медосмотра',
    'ожидает предрейсового техосмотра',
    'ожидает выпуска диспетчером',
    'в рейсе',
    'ожидает послерейсового медосмотра',
    'ожидает послерейсового техосмотра',
    'ожидает отметки о возвращении диспетчером'
]);

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/return-for-correction`, formData);
    toast.warn('Путевой лист возвращен на доработку!');
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