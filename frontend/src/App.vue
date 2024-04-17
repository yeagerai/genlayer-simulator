<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
</script>
<template>
  <main data-mode="light" class="h-screen bg-white dark:bg-gray-dark flex flex-col">
    <Header />
    <div class="flex h-screen">
      <RouterView />
    </div>
  </main>
  <notifications />
</template>

<style scoped></style>
