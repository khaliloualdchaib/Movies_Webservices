<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Sidenav from './components/SidenavComponent.vue';
</script>

<template>
  <div>
    <Sidenav></Sidenav>
    <div class="p-4 sm:ml-64">
      <div class="p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700">
        <RouterView></RouterView>
      </div>
    </div>
  </div>
</template>