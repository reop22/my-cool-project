<!-- ПУТЬ: frontend/src/components/forms/PreTripTechnicalForm.vue -->
<template>
  <Fieldset legend="Действие: Предрейсовый технический контроль" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12 md:col-6">
        <label for="odometer-start">Показания одометра при выезде (км)</label>
        <InputNumber id="odometer-start" v-model="formData.departure_odometer" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="fuel-start">Остаток горючего при выезде (л)</label>
        <InputNumber id="fuel-start" v-model="formData.fuel_balance_start" required mode="decimal" :minFractionDigits="1" />
      </div>
      <!-- ДОБАВЛЕНО НОВОЕ ПОЛЕ -->
      <div class="field col-12">
        <label for="control-notes">Заметка о предрейсовом контроле</label>
        <InputText id="control-notes" v-model="formData.pre_trip_control_notes" required />
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-check" label="Автомобиль исправен, передать диспетчеру" />
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
import InputText from 'primevue/inputtext'; // <-- Добавлен импорт

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);

// ДОБАВЛЕНО НОВОЕ ПОЛЕ В ОБЪЕКТ
const formData = reactive({
  departure_odometer: null,
  fuel_balance_start: null,
  pre_trip_control_notes: 'Технически исправен', // <-- Значение по умолчанию
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/pre-trip-technical`, formData);
    toast.success('Данные техконтроля успешно внесены!');
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