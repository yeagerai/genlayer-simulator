<script setup lang="ts">
import { notify } from "@kyvg/vue3-notification";
const handleNotify = () => {
  notify("Hello user!");
}
</script>
<template>
  <main>
  Contracts
  <button @click="handleNotify">Notify</button>
  </main>
</template>
