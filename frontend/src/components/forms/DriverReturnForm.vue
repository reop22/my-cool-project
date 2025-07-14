<!-- ПУТЬ: frontend/src/components/forms/DriverReturnForm.vue -->
<template>
  <Fieldset legend="Действие: Заполнение данных по возвращении" :toggleable="true">
    <form @submit.prevent="handleSubmit">
      <h3 class="mt-0">Результаты работы автомобиля за смену (оборотная сторона)</h3>
      
      <!-- Убираем режим редактирования, делаем поля всегда активными -->
      <div class="p-datatable p-component">
        <div class="p-datatable-wrapper">
          <table class="p-datatable-table">
            <thead class="p-datatable-thead">
              <tr>
                <th>Номер заказчика</th>
                <th>Отправление</th>
                <th>Назначение</th>
                <th>Время выезда</th>
                <th>Время возвращ.</th>
                <th>Пробег, км</th>
                <th></th>
              </tr>
            </thead>
            <tbody class="p-datatable-tbody" v-auto-animate>
              <tr v-for="(point, index) in routePoints" :key="point.id">
                <td><InputText v-model="point.customer_number" class="w-full" /></td>
                <td><InputText v-model="point.departure_point" class="w-full" /></td>
                <td><InputText v-model="point.arrival_point" class="w-full" /></td>
                <td><InputText v-model="point.departure_time" class="w-full" /></td>
                <td><InputText v-model="point.arrival_time" class="w-full" /></td>
                <td><InputNumber v-model="point.distance" mode="decimal" class="w-full" /></td>
                <td>
                  <Button icon="pi pi-trash" outlined rounded severity="danger" @click="removePoint(index)" />
                </td>
              </tr>
              <tr v-if="!routePoints.length">
                <td colspan="7" class="text-center py-4">Нажмите "Добавить строку маршрута", чтобы начать.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <Button icon="pi pi-plus" label="Добавить строку маршрута" @click="addPoint" class="mt-2" severity="secondary" outlined />
      
      <div class="mt-4">
        <Button type="submit" label="Подтвердить данные и передать на медосмотр" :loading="loading" class="w-full p-button-lg" />
      </div>
    </form>
  </Fieldset>
</template>

<script setup>
import { ref } from 'vue';
import apiClient from '../../services/api';
import { useToast } from 'vue-toastification';
import Fieldset from 'primevue/fieldset';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';

const props = defineProps({ sheetId: Number });
const emit = defineEmits(['update-successful']);
const toast = useToast();

const routePoints = ref([]);
const loading = ref(false);
let nextId = 0;

const addPoint = () => {
  routePoints.value.push({
    id: nextId++,
    customer_number: '',
    departure_point: '',
    arrival_point: '',
    departure_time: '',
    arrival_time: '',
    distance: null, 
    cargo_weight: null,
  });
};

const removePoint = (index) => {
  routePoints.value.splice(index, 1);
};

const handleSubmit = async () => {
  loading.value = true;
  try {
    const payload = { 
      route_points: routePoints.value.map(({ id, ...rest }) => ({
        ...rest,
        distance: rest.distance || 0,
        cargo_weight: rest.cargo_weight || 0,
      }))
    };
    await apiClient.patch(`/trip-sheets/${props.sheetId}/driver-return`, payload);
    toast.success('Данные по рейсу успешно сохранены!');
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
/* Добавляем стили для кастомной таблицы, чтобы она была похожа на DataTable */
.p-datatable-table {
  width: 100%;
  border-collapse: collapse;
}
.p-datatable-thead > tr > th {
  padding: 1rem;
  border: 1px solid var(--surface-border);
  border-width: 0 0 1px 0;
  font-weight: 600;
  text-align: left;
  background-color: var(--surface-a);
}
.p-datatable-tbody > tr > td {
  padding: 0.5rem;
  border: 1px solid var(--surface-border);
  border-width: 0 0 1px 0;
}
.text-center {
  text-align: center;
}
</style>