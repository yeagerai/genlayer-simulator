<script setup>
import LoadingIndicator from '@/components/LoadingIndicator.vue'

const emit = defineEmits(['click'])
const props = defineProps({
    id: { type: String, default: null },
    disabled: { type: Boolean, default: false },
    loading: { type: Boolean, default: false }
})
</script>

<template>
    <button :id="id" class="flex items-center justify-center gap-2 bg-primary dark:bg-accent hover:bg-opacity-90 text-white font-semibold px-4 py-2 rounded"
        :disabled="disabled || loading" @click="emit('click')">
        <LoadingIndicator v-if="loading" color="white" />
        <slot />
    </button>
</template>