<script setup lang="ts">

</script>

<template>
  <div class="flex flex-col overflow-y-auto max-h-[93vh]">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Settings</h3>
    </div>
    <div class="flex justify-between items-center p-2">
      <div class="flex">
        Number of validators
      </div>
      <div class="flex justify-end">
        <input type="number" class="bg-slate-100 dark:dark:bg-zinc-700 p-2 w-12" label="Number of validators"
          value="5" />
      </div>
    </div>
  </div>
</template>
