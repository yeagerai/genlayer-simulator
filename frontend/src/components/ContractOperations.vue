<script setup lang="ts">

</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-toolbar-title>Contract Operations</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-list lines="one">
      <v-list-item>
        <template v-slot:prepend>
          <v-list-item-action start>
            <v-btn>store()</v-btn>
          </v-list-item-action>
        </template>
        <v-text-field label="1"></v-text-field>
      </v-list-item>
      <v-list-item>
        <template v-slot:prepend>
          <v-list-item-action start>
            <v-btn>retrieve()</v-btn>
          </v-list-item-action>
        </template>

      </v-list-item>
    </v-list>
  </v-card>
</template>
<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
