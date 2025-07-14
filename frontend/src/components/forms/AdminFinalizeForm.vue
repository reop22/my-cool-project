<!-- ПУТЬ: frontend/src/components/forms/AdminFinalizeForm.vue -->
<template>
  <Fieldset legend="Действие Администратора: Финальные расчеты" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <p>Введите финальные расчетные данные. Расход по факту будет рассчитан автоматически на сервере.</p>
      <div class="field col-12 md:col-6">
        <label for="consumption-norm">Расход по норме, л</label>
        <InputNumber id="consumption-norm" v-model="formData.fuel_consumption_norm" mode="decimal" />
      </div>
       <div class="field col-12 md:col-6">
        <label for="salary-notes">Расчет заработной платы</label>
        <InputText id="salary-notes" v-model="formData.salary_calculation_notes" />
      </div>
       <div class="field col-12">
        <label for="work-results">Результаты работы автомобиля и прицепов</label>
        <Textarea id="work-results" v-model="formData.work_results_notes" rows="3" autoResize />
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-verified" label="Утвердить и сделать доступным для скачивания" severity="success" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from 'vue-toastification';
import Fieldset from 'primevue/fieldset';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);
const formData = reactive({
  fuel_consumption_norm: null,
  salary_calculation_notes: '',
  work_results_notes: ''
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/admin-final`, formData);
    toast.success('Путевой лист финализирован и доступен для скачивания!');
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
</style>