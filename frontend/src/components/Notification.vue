<script setup>
import { XMarkIcon } from '@heroicons/vue/16/solid';
</script>

<template>
  <notifications position="bottom right">
    <template #body="props">
      <div
        class="relative mt-[10px] rounded border-l-4 p-2 text-sm text-white"
        :class="[
          !props.item.type && 'border-blue-400 bg-slate-600',
          props.item.type === 'success' && 'border-green-400 bg-emerald-600',
          props.item.type === 'warn' && 'border-yellow-600 bg-amber-500',
          props.item.type === 'error' && 'border-red-600 bg-red-500',
        ]"
      >
        <div class="font-medium">
          {{ props.item.title }}
        </div>

        <button
          @click="props.close"
          class="absolute right-[3px] top-[3px] rounded-full p-[5px] opacity-75 hover:opacity-100"
        >
          <XMarkIcon class="h-4 w-4 text-white" />
        </button>

        <div class="text-xs">
          {{ props.item.text }}
        </div>
      </div>
    </template>
  </notifications>
</template>

<style lang="css">
.vue-notification-group {
  margin: 65px 10px 10px;
}
</style>
