<script setup lang="ts">
import { XMarkIcon } from '@heroicons/vue/24/solid'

</script>

<template>
    <div class="flex flex-col w-full">
        <nav class="border-b text-sm flex justify-start">
            <button class="flex justify-between px-2 py-2 border-b-2 border-primary text-primary font-semibold">
                <div>Contract Name</div>
                <XMarkIcon class="ml-4 h-4 w-4" />
            </button>
            <!-- <button class="inline-block px-4 py-2 text-gray-700 hover:text-black" href="#">Tab 3</button> -->
        </nav>
    </div>
</template>
