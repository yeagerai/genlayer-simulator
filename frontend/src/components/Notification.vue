<script setup>
import { XMarkIcon } from '@heroicons/vue/16/solid';
</script>

<template>
    <notifications position="top right">
        <template #body="props">
            <div class="rounded p-2 text-sm mt-[10px] text-white relative border-l-4 " :class="[
                !props.item.type && 'bg-slate-600 border-blue-400',
                props.item.type === 'success' && 'bg-emerald-600 border-green-400',
                props.item.type === 'warn' && 'bg-amber-500 border-yellow-600',
                props.item.type === 'error' && 'bg-red-500 border-red-600'
            ]">

                <div class="font-medium">
                    {{ props.item.title }}
                </div>

                <button @click="props.close"
                    class="absolute top-[3px] right-[3px] p-[5px] rounded-full opacity-75 hover:opacity-100">
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