<script setup lang="ts">
import { RouterView } from 'vue-router'
import logo from '@/assets/genlayer.png'
</script>

<template>
  <v-app>
    <v-container fluid class="m-0 p-0">
      <v-app-bar :elevation="2" rounded>
        <template v-slot:prepend>
          <img :src="logo" alt="" width="180">
        </template>
        <v-app-bar-title></v-app-bar-title>
      </v-app-bar>
      <RouterView class="mt-12" />
    </v-container>
    <v-footer border>
      <v-row justify="center" no-gutters>
        <v-col class="text-center mt-4" cols="12">
          {{ new Date().getFullYear() }} — <strong>GenLayer</strong>
        </v-col>
      </v-row></v-footer>
  </v-app>
</template>

<style scoped></style>
