<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from '@/components/HeaderComponent.vue'
import { useUIStore } from '@/stores/ui'
import { onBeforeMount } from 'vue';
const uiStore = useUIStore()
onBeforeMount(() => {
  uiStore.initialize()
})
</script>
<template>
  <main :data-mode="uiStore.mode" class="h-screen w-full bg-white dark:bg-zinc-800 dark:text-white flex flex-col">
    <Header />
    <div class="flex h-full">
      <RouterView />
    </div>
  </main>
  <notifications />
</template>
