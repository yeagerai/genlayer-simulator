<script setup lang="ts">
import { RouterView } from 'vue-router';
import Header from '@/components/Header.vue';
import Notification from '@/components/Notification.vue';
import TutorialContainer from '@/components/Tutorial/TutorialContainer.vue';
import { useUIStore } from '@/stores/ui';
import { onBeforeMount } from 'vue';
import { useSetupStores } from '@/hooks';

const uiStore = useUIStore();
const { setupStores } = useSetupStores();

onBeforeMount(() => {
  uiStore.initialize();
  setupStores();
});
</script>

<template>
  <TutorialContainer />
  <main class="flex h-screen w-full flex-col">
    <Header />
    <div class="flex" :style="{ height: 'calc(100vh - 53px)' }">
      <RouterView />
    </div>
  </main>
  <Notification />
</template>
