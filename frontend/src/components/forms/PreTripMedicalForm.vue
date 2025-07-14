<!-- ПУТЬ: frontend/src/components/forms/PreTripMedicalForm.vue -->
<template>
  <Fieldset legend="Действие: Предрейсовый медосмотр" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12">
        <label for="doctor-license">Номер лицензии медучреждения</label>
        <InputText id="doctor-license" v-model="formData.pre_trip_doctor_license" required />
      </div>
      <div class="col-12">
        <Button 
          type="submit"
          :loading="loading" 
          label="Водитель допущен, передать механику" 
          icon="pi pi-check" 
          severity="success"
        />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { reactive, ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from 'vue-toastification';
import Fieldset from 'primevue/fieldset';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';

const props = defineProps({ sheetId: { type: Number, required: true } });
const emit = defineEmits(['update-successful']);
const toast = useToast();
const loading = ref(false);

// Добавляем поле для лицензии
const formData = reactive({
  pre_trip_doctor_license: ''
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    // Отправляем данные формы в теле запроса
    await apiClient.patch(`/trip-sheets/${props.sheetId}/pre-trip-medical`, formData);
    toast.success('Отметка о медосмотре успешно поставлена!');
    emit('update-successful');
  } catch (err) {
    let errorMessage = 'Ошибка.';
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