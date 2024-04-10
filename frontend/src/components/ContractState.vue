<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps({
  contractState: { type: Object, default: () => { } }
})

const stateItems = ref<{ name: string, value: any }[]>([]);

watch(() => props.contractState,
  (newValue) => {
    if (newValue && Object.keys(newValue).length > 0) {
      stateItems.value = Object.entries(newValue).map((item) => ({ name: item[0], value: item[1] }));
    }
  }
)
</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-toolbar-title>Intelligent Contract State</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-table height="320px" fixed-header>
      <thead>
        <tr>
          <th class="text-left">
            Name
          </th>
          <th class="text-left">
            Value
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in stateItems" :key="item.name">
          <td>{{ item.name }}</td>
          <td>{{ item.value }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>
<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
