<!-- ПУТЬ: frontend/src/components/forms/PostTripMedicalForm.vue -->
<template>
  <Fieldset legend="Действие: Послерейсовый медосмотр" :toggleable="true">
    <form @submit.prevent="handleSubmit" class="p-fluid grid">
      <div class="field col-12">
        <label for="doctor-license">Номер лицензии медучреждения</label>
        <InputText id="doctor-license" v-model="formData.post_trip_doctor_license" required />
      </div>
      <div class="col-12">
        <Button type="submit" :loading="loading" icon="pi pi-check" label="Водитель здоров, передать механику" severity="success" />
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
const formData = reactive({
  post_trip_doctor_license: ''
});

const handleSubmit = async () => {
  loading.value = true;
  try {
    await apiClient.patch(`/trip-sheets/${props.sheetId}/post-trip-medical`, formData);
    toast.success('Отметка о послерейсовом медосмотре успешно поставлена!');
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