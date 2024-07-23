<script setup lang="ts">
import { XMarkIcon } from '@heroicons/vue/24/solid'
const props = defineProps({
  open: { type: Boolean, default: false },
})
</script>

<template>
  <div
    v-show="props.open"
    className="fixed top-0 left-0 flex justify-center items-center w-full h-full bg-black bg-opacity-50 z-50"
  >
    <div
      className="relative bg-white rounded-lg p-8 dark:bg-zinc-800 dark:text-white text-primary min-w-[30%] max-w-[70%]"
    >
      <button
        className="absolute top-2 right-2 hover:text-gray-500 focus:outline-none dark:bg-zinc-800 dark:text-white text-primary"
        @click="$emit('close')"
      >
        <XMarkIcon class="ml-4 h-4 w-4" />
      </button>
      <div class="flex flex-col">
        <slot></slot>
      </div>
    </div>
  </div>
</template>
