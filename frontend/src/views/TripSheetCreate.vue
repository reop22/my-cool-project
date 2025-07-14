<!-- ПУТЬ: frontend/src/views/TripSheetCreate.vue -->
<template>
  <div class="create-container container">
    <PageHeader title="Новый путевой лист" subtitle="Заполните первичные данные. Остальные поля будут заполнены на следующих этапах." />
    <Card>
      <template #content>
        <form @submit.prevent="handleSubmit" class="p-fluid grid" v-auto-animate>
          <div class="field col-12 md:col-6">
            <label for="series">Серия путевого листа</label>
            <InputText id="series" v-model="form.series" required />
          </div>
          <div class="field col-12 md:col-6">
            <label for="reg-number">Регистрационный номер</label>
            <InputText id="reg-number" v-model="form.registration_number" required />
          </div>
          
          <Divider align="center" type="dashed"><b>Организация</b></Divider>

          <div class="field col-12">
            <label for="org-name">Наименование организации</label>
            <InputText id="org-name" v-model="form.organization_name" required />
          </div>
          <div class="field col-12 md:col-8">
            <label for="org-address">Адрес организации</label>
            <InputText id="org-address" v-model="form.organization_address" required />
          </div>
           <div class="field col-12 md:col-4">
            <label for="org-phone">Телефон организации</label>
            <InputText id="org-phone" v-model="form.organization_phone" required />
          </div>
          <div class="field col-12">
            <label for="org-okpo">ОКПО</label>
            <InputText id="org-okpo" v-model="form.organization_okpo" required />
          </div>
          
          <Divider align="center" type="dashed"><b>Автомобиль и перевозка</b></Divider>

          <div class="field col-12 md:col-6">
            <label for="car-model">Марка, модель автомобиля</label>
            <InputText id="car-model" v-model="form.car_model" required />
          </div>
           <div class="field col-12 md:col-3">
            <label for="car-plate">Гос. номер</label>
            <InputText id="car-plate" v-model="form.car_plate" required />
          </div>
          <div class="field col-12 md:col-3">
            <label for="garage-number">Гаражный номер</label>
            <InputText id="garage-number" v-model="form.garage_number" required />
          </div>
           <div class="field col-12">
            <label for="comm-type">Вид сообщения</label>
            <InputText id="comm-type" v-model="form.communication_type" required />
          </div>

          <Divider align="center" type="dashed"><b>Данные водителя</b></Divider>
          
          <div class="field col-12 md:col-6">
            <label for="license">Номер В/У</label>
            <InputText id="license" v-model="form.driver_license_number" required />
          </div>
           <div class="field col-12 md:col-6">
            <label for="license-type">Тип лицензионной карточки</label>
            <Dropdown id="license-type" v-model="form.driver_license_type" :options="['стандартная', 'ограниченная']" placeholder="Выберите тип" required />
          </div>
          <div class="field col-12 md:col-6">
            <label for="personnel-number">Табельный номер</label>
            <InputText id="personnel-number" v-model="form.driver_personnel_number" required />
          </div>
           <div class="field col-12 md:col-6">
            <label for="snils">СНИЛС</label>
            <InputText id="snils" v-model="form.driver_snils" required />
          </div>
           <div class="field col-12 md:col-6">
            <label for="class">Класс</label>
            <InputText id="class" v-model="form.driver_class" required />
          </div>

          <div class="col-12 mt-4">
            <!-- ИЗМЕНЕНИЕ ЗДЕСЬ -->
            <Button type="submit" :loading="loading" label="Сохранить черновик" icon="pi pi-save" class="w-full p-button-lg" />
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';
import { useToast } from "vue-toastification";
import PageHeader from '../components/PageHeader.vue';
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import Dropdown from 'primevue/dropdown';

const router = useRouter();
const toast = useToast();
const form = reactive({
  series: '',
  organization_name: '',
  organization_address: '',
  organization_okpo: '',
  organization_phone: '',
  registration_number: '',
  communication_type: '',
  car_model: '',
  car_plate: '',
  garage_number: '',
  driver_license_number: '',
  driver_license_type: 'стандартная',
  driver_class: '',
  driver_snils: '',
  driver_personnel_number: '',
});
const loading = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  try {
    const response = await apiClient.post('/trip-sheets/', form);
    // ИЗМЕНЕНИЕ ЗДЕСЬ
    toast.success('Черновик путевого листа успешно сохранен!');
    router.push(`/trip-sheets/${response.data.id}`);
  } catch (err) {
    let errorMessage = 'Ошибка создания.';
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