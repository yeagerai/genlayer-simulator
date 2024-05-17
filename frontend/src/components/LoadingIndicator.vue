<script setup lang="ts">
import { useUIStore } from '@/stores'
const uiStore = useUIStore()
const props = defineProps<{ color?: string }>()
</script>
<template>
    <div class="flex items-center flex-col">
        <VueSpinnerOval size="25" :color="props.color ? props.color : (uiStore.mode === 'light' ? '#1a3851' : 'white')"
            width="50" />
        <slot />
    </div>
</template>