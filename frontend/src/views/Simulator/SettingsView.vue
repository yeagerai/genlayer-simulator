<script setup lang="ts">
import { useConfig } from '@/hooks';
import MainTitle from '@/components/Simulator/MainTitle.vue';
import ProviderSection from '@/components/Simulator/settings/ProviderSection.vue';
import SimulatorSection from '@/components/Simulator/settings/SimulatorSection.vue';

const { canUpdateProviders, studioVersion } = useConfig();
</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <MainTitle data-testid="settings-page-title"
      >Settings

      <template #actions>
        <div class="font-mono text-[10px] opacity-40">
          {{ studioVersion }}
        </div>
      </template>
    </MainTitle>

    <SimulatorSection />
    <ProviderSection v-if="canUpdateProviders" />
  </div>
</template>
