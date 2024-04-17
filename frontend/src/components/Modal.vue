<script setup lang="ts">
const props = defineProps({
    open: { type: Boolean, default: false }
})

</script>
<template>
    <div v-if="props.open"
        className="fixed top-0 left-0 flex justify-center items-center w-full h-full bg-black bg-opacity-50 z-50">
        <div className="relative bg-white border border-black rounded-lg p-8">
            <button className="absolute top-2 right-2 text-black hover:text-gray-500 focus:outline-none"
                @click="$emit('close')">
                <MdClose className="text-2xl" />
            </button>
            <div class="flex flex-col">
                <slot></slot>
            </div>
        </div>
    </div>
    <div v-else />
</template>