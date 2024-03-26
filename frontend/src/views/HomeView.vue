<script setup lang="ts">
import CodeEditor from '@/components/CodeEditor.vue'
</script>

<template>
  <v-container fluid class="m-0 p-0">
    <v-row>
      <v-col>1</v-col>
      <v-col>
        <v-container class="m-0 p-0">
          <v-row>
            Buttons
          </v-row>
          <v-row>
            <v-col>
              <CodeEditor></CodeEditor>
            </v-col>
          </v-row>
        </v-container>
      </v-col>
    </v-row>
    <v-row>
      <v-col>1</v-col>
      <v-col>2</v-col>
    </v-row>
  </v-container>
</template>
