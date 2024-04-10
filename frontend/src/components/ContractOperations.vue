<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { InputTypesMap } from '@/utils'

interface Abi {
  methods: {
    [k: string]: {
      inputs: { [k: string]: string }
    }
  },
  class: string
}

interface Props {
  abi: Abi
}

const props = defineProps<Props>();
const emit = defineEmits(['callMethod']);

const methodList = computed(() => {
  return Object.entries(props.abi?.methods || {})
  .filter(m => m[0] !== 'call_llm').map(m => ({
    name: m[0],
    inputs: m[1].inputs
  }))
})
const inputs = ref<{ [k: string]: any }>({});

const handleMethodCall = (method: string) => {
  const params = Object.values(inputs.value[method] || {})
  emit('callMethod', {method, params})
}

watch(
  () => props.abi?.methods,
  () => {
    inputs.value = methodList.value.reduce((prev: any, curr) => {
      prev[curr.name] = {};
      return prev
    }, {})
  },
);

</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-toolbar-title>Contract Operations</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-container fluid>
      <v-row>
        <v-col>
          <h3>Contract: <b>{{ props.abi?.class }}</b></h3>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-list lines="one">
            <v-list-item v-for="method in methodList" :key="method.name">
              <template v-slot:prepend>
                <v-list-item-action start>
                  <v-btn @click="handleMethodCall(method.name)">{{ method.name }}()</v-btn>
                </v-list-item-action>
              </template>
              <template v-for="(inputType, input) in method.inputs" :key="input">
                <v-checkbox v-if="inputType === 'bool'" :label="`${input}`"
                  v-model="inputs[method.name][input]"></v-checkbox>
                <v-text-field v-else :key="input" :type="InputTypesMap[inputType]" :label="`${input}`"
                  v-model="inputs[method.name][input]" />
              </template>

            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
