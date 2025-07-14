<!-- ПУТЬ: frontend/src/components/TripSheetListSkeleton.vue -->
<template>
  <DataTable :value="new Array(5)" responsiveLayout="scroll">
    <Column header="Номер листа"><template #body><Skeleton></Skeleton></template></Column>
    <Column header="Дата создания"><template #body><Skeleton></Skeleton></template></Column>
    <Column header="Водитель"><template #body><Skeleton></Skeleton></template></Column>
    <Column header="Автомобиль"><template #body><Skeleton></Skeleton></template></Column>
    <Column header="Действие"><template #body><Skeleton width="10rem" height="2rem"></Skeleton></template></Column>
  </DataTable>
</template>

<script setup>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Skeleton from 'primevue/skeleton';
</script>