<script setup lang="ts">
import { RouterView } from 'vue-router';
import Header from '@/components/Header.vue';
import Notification from '@/components/Notification.vue';
import TutorialContainer from '@/components/Tutorial/TutorialContainer.vue';
import { useUIStore } from '@/stores/ui';
import { onBeforeMount } from 'vue';

const uiStore = useUIStore();
onBeforeMount(() => {
  uiStore.initialize();
});
</script>

<template>
  <TutorialContainer />
  <main class="flex h-screen w-full flex-col">
    <Header />
    <div class="flex h-full">
      <RouterView />
    </div>
  </main>
  <Notification />
</template>
