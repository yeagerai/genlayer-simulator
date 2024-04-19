<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  contractState: { type: Object, default: () => { } }
})

const stateItems = ref<{ name: string; value: any }[]>([])

watch(
  () => props.contractState,
  (newValue) => {
    if (newValue && Object.keys(newValue).length > 0) {
      stateItems.value = Object.entries(newValue).map((item) => ({ name: item[0], value: item[1] }))
    }
  }
)
</script>
<template>
  <div class="flex flex-col w-full px-1">
    <div class="flex justify-between" v-for="item in stateItems" :key="item.name">
      <div class="flex">{{ item.name }}: </div>
      <div class="flex">{{ item.value }}</div>
    </div>
  </div>
  </template>
  <style>
  
  </style>
