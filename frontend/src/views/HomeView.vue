<script setup lang="ts">
import CodeEditor from '@/components/CodeEditor.vue'
import ContractState from '@/components/ContractState.vue'
import NodeLogs from '@/components/NodeLogs.vue'
import ContractOperations from '@/components/ContractOperations.vue'
</script>

<template>
  <v-container fluid class="m-0 p-0">
    <v-row>
      <v-col>
        <ContractState />
      </v-col>
      <v-col>
        <CodeEditor />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <ContractOperations />
      </v-col>
      <v-col>
        <NodeLogs />
      </v-col>
    </v-row>
  </v-container>
</template>
