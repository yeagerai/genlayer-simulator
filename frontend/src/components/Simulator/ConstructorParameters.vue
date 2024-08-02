<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { InputTypesMap } from '@/utils';
import { notify } from '@kyvg/vue3-notification';
import { useUIStore } from '@/stores';
import { ArrowUpTrayIcon } from '@heroicons/vue/16/solid';
import { ExclamationTriangleIcon } from '@heroicons/vue/24/solid';

interface Props {
  inputs: { [k: string]: string };
  loading: boolean;
  error?: Error;
  deploying: boolean;
}

// TODO: check if we need to update again also we have an issue with conversion
// between `bool` in Python with value `True` vs JSON boolean with value `true`

const mapInputs = (inputs: { [k: string]: string }) =>
  Object.keys(inputs || {})
    .map((key) => ({ name: key, type: InputTypesMap[key], value: inputs[key] }))
    .reduce((prev, curr) => {
      if (typeof curr.value === 'boolean') {
        prev = { ...prev, [curr.name]: curr.value ? 'True' : 'False' };
      } else {
        prev = { ...prev, [curr.name]: curr.value };
      }

      return prev;
    }, {});

const setInputParams = (inputs: { [k: string]: string }) => {
  inputParams.value = Object.keys(inputs)
    .map((key) => ({ name: key, value: inputs[key] }))
    .reduce((prev, curr) => {
      switch (curr.value) {
        case 'bool':
          prev = { ...prev, [curr.name]: false };
          break;
        case 'str':
          prev = { ...prev, [curr.name]: '' };
          break;
        case 'int':
          prev = { ...prev, [curr.name]: 0 };

          break;
        case 'float':
          prev = { ...prev, [curr.name]: 0.0 };

          break;
        default:
          prev = { ...prev, [curr.name]: '' };
          break;
      }
      return prev;
    }, {});

  jsonParams.value = JSON.stringify(inputParams.value || {}, null, 2);
};
const jsonParams = ref('{}');
const inputParams = ref<{ [k: string]: any }>({});
const props = defineProps<Props>();
const emit = defineEmits(['deployContract']);
const mode = ref<'json' | 'form'>('form');
const uiStore = useUIStore();
const handleDeployContract = () => {
  if (mode.value === 'json') {
    try {
      const json = JSON.parse(jsonParams.value || '{}');
      const params = mapInputs(json);
      emit('deployContract', { params });
    } catch (error) {
      console.error(error);
      notify({
        title: 'Error',
        text: 'You should provide a valid json',
        type: 'error',
      });
    }
  } else {
    const params = mapInputs(inputParams.value || {});
    emit('deployContract', { params });
  }
};
const toggleMode = () => {
  mode.value = mode.value === 'json' ? 'form' : 'json';
  if (mode.value === 'json') {
    jsonParams.value = JSON.stringify(inputParams.value || {}, null, 2);
  } else {
    inputParams.value = JSON.parse(jsonParams.value || '{}');
  }
};

watch(
  () => props.inputs,
  (newValue) => {
    setInputParams(newValue || {});
  },
);

onMounted(() => {
  if (props.inputs) {
    setInputParams(props.inputs);
  }
});
</script>

<template>
  <div v-if="props.error">
    <div class="my-4 flex flex-col p-2">
      <div class="flex flex-col">
        <div class="flex flex-col justify-between align-middle">
          <div class="flex h-full align-middle text-xs">
            Constructor Parameters
          </div>
          <div
            class="dark:color-neutral-100 flex flex-col items-center p-5 text-xs text-red-500"
          >
            <ExclamationTriangleIcon class="h-6 w-6" /> Error Loading
            Constructor Parameters please refresh the page and try again.
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="props.loading">
    <div class="my-4 flex flex-col p-2">
      <div class="flex flex-col">
        <div class="flex flex-col justify-between align-middle">
          <div class="flex h-full align-middle text-xs">
            Constructor Parameters
          </div>
          <div class="flex flex-col items-center p-5">
            <VueSpinnerOval
              size="30"
              :color="uiStore.mode === 'light' ? '#1a3851' : 'white'"
              width="50"
            />
            Loading...
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="my-4 flex flex-col p-2">
      <div class="flex flex-col">
        <div class="flex justify-between align-middle">
          <div class="flex h-full align-middle text-xs">
            Constructor Parameters
          </div>
          <!-- TODO: re-implement json mode -->
          <button
            class="texm-xs rounded bg-primary px-2 text-white hover:opacity-80"
            @click="toggleMode"
          >
            {{ mode === 'json' ? 'Inputs' : 'JSON' }}
            <ToolTip
              :text="mode === 'json' ? 'See the inputs' : 'Write raw JSON'"
              :options="{ placement: 'top' }"
            />
          </button>
        </div>
        <p v-if="mode === 'json'" class="text-xs">
          Please provide a JSON object with the constructor parameters.
        </p>
      </div>
      <div class="mt-2 flex" v-if="mode === 'json'">
        <textarea
          rows="5"
          class="w-full bg-slate-100 p-2 dark:dark:bg-zinc-700"
          v-model="jsonParams"
          clear-icon="ri-close-circle"
          label="State"
        />
      </div>
      <div class="mt-2 flex flex-col" v-else>
        <div
          class="flex items-center justify-between py-2"
          v-for="(inputType, input) in props.inputs"
          :key="input"
        >
          <label :for="`${input}`" class="mr-2 text-xs">{{ input }}</label>
          <input
            v-model="inputParams[input]"
            :name="`${input}`"
            :type="InputTypesMap[inputType]"
            :placeholder="`${input}`"
            class="bg-slate-100 p-2 dark:dark:bg-zinc-700"
            label="Input"
          />
        </div>
      </div>
    </div>
    <div class="flex w-full flex-col justify-center p-2">
      <Btn
        testId="btn-deploy-contract"
        @click="handleDeployContract"
        :loading="deploying"
      >
        <ArrowUpTrayIcon class="h-4 w-4" />
        {{ deploying ? 'Deploying...' : 'Deploy' }}
      </Btn>
    </div>
  </div>
</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
