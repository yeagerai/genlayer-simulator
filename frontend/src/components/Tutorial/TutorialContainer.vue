<script setup lang="ts">
import { useRouter } from 'vue-router';
import { DEFAULT_OPTIONS, KEYS } from './constants';
import TutorialStep from './TutorialStep.vue';
import { useContractsStore, useTutorialStore, useUIStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';

const contractsStore = useContractsStore();
const tutorialStore = useTutorialStore();
const uiStore = useUIStore();
const router = useRouter();
const contract = computed(() => contractsStore.contracts[0]);
const contracts = computed(() => contractsStore.contracts);
const steps = ref([
  {
    target: '#tutorial-welcome',
    header: {
      title: 'Welcome to GenLayer Simulator!',
    },
    content:
      'This tutorial will guide you through the basics. Click “Next” to begin!',
    onNextStep: async () => {
      contractsStore.openFile(contract.value?.id);
    },
  },
  {
    target: `.contract-item`,
    header: {
      title: 'Code Editor',
    },
    content: `Write and edit your Intelligent Contracts here. This example contract is preloaded for you.`,
    onNextStep: async () => {
      router.push({ name: 'run-debug', query: { tutorial: 1 } });
    },
  },
  {
    target: '#tutorial-how-to-deploy',
    header: {
      title: 'Deploying Contracts',
    },
    content:
      'Click “Next” to automatically deploy your Intelligent Contract to the GenLayer network.',
    onNextStep: async () => {
      await tutorialStore.deployContract();
      notify({
        title: 'OK',
        text: 'Contract deployed',
        type: 'success',
      });
    },
  },
  {
    target: '#tutorial-creating-transactions',
    header: {
      title: 'Creating Transactions',
    },
    content:
      'This is where you can interact with the deployed contract. You can select a method you want to use from the dropdown, and provide the parameters.  Click “Next” to automatically create a transaction and interact with your deployed contract.',
    onNextStep: async () => {
      tutorialStore.callContractMethod();
      notify({
        title: 'OK',
        text: 'Contract method called',
        type: 'success',
      });
    },
  },
  {
    target: '#tutorial-node-output',
    header: {
      title: 'Node Output',
    },
    content:
      'View real-time feedback as your transaction execution and debug any issues.',
  },

  {
    target: '#tutorial-contract-state',
    header: {
      title: 'Contract State',
    },
    content:
      "This panel shows the contract's data after executing transactions.",
  },
  {
    target: '#tutorial-tx-response',
    header: {
      title: 'Transaction Response',
    },
    content:
      'See the results of your transaction interaction with the contract in this area.',
    onNextStep: async () => {
      router.push({ name: 'contracts' });
    },
  },
  {
    header: {
      title: 'Switching Examples',
    },
    target: '#tutorial-how-to-change-example',
    content:
      'Switch between different example contracts to explore various features and functionalities.',
    onNextStep: async () => {
      await router.push({ name: 'settings' });
    },
  },
  {
    header: {
      title: 'Validators',
    },
    target: '#tutorial-validators',
    content:
      'Configure the number of validators and set up their parameters here.',
  },
  {
    header: {
      title: 'Congratulations!',
    },
    target: '#tutorial-end',
    content:
      "You've completed the GenLayer Simulator tutorial. Feel free to revisit any step or start experimenting with your own contracts. Happy coding!",
  },
]);

const currentStep = ref(-1);
const options = ref(DEFAULT_OPTIONS);
const numberOfSteps = computed(() => steps.value.length);
const isRunning = computed(() => {
  return currentStep.value > -1 && currentStep.value < numberOfSteps.value;
});
const isFirst = computed(() => currentStep.value === 0);
const isLast = computed(() => currentStep.value === steps.value.length - 1);
const step = computed(() => steps.value[currentStep.value]);
const showTutorial = computed(() => uiStore.showTutorial);

function stop() {
  document.body.classList.remove('v-tour--active');
  currentStep.value = -1;
}

function skip() {
  stop();
}

function finish() {
  stop();
}

function isKeyEnabled(key: 'escape' | 'arrowRight' | 'arrowLeft'): boolean {
  if (
    options.value.enabledNavigationKeys &&
    options.value.enabledNavigationKeys[key]
  ) {
    return options.value.enabledNavigationKeys[key];
  }
  return false;
}

function handleKeyup(e: KeyboardEvent) {
  if (options.value.debug) {
    console.log('[Vue Tour] A keyup event occured:', e);
  }
  switch (e.keyCode) {
    case KEYS.ARROW_RIGHT:
      isKeyEnabled('arrowRight') && nextStep();
      break;
    case KEYS.ARROW_LEFT:
      isKeyEnabled('arrowLeft') && previousStep();
      break;
    case KEYS.ESCAPE:
      isKeyEnabled('escape') && stop();
      break;
  }
}
async function start(startStep?: number) {
  router.replace({ name: 'contracts' });
  contractsStore.setCurrentContractId('');
  // Register keyup listeners for this tour
  if (options.value.useKeyboardNavigation) {
    window.addEventListener('keyup', handleKeyup);
  }
  localStorage.setItem('genlayer.tutorial', new Date().getTime().toString());

  // Wait for the DOM to be loaded, then start the tour
  startStep = startStep ? parseInt(`${startStep}`, 10) : 0;
  let step = steps.value[startStep];

  let process = () =>
    new Promise((resolve, _reject) => {
      setTimeout(() => {
        contractsStore.openFile(contracts.value[0].id);
        currentStep.value = startStep;
        resolve(0);
      }, options.value.startTimeout);
    });

  if ((step as any).before) {
    try {
      await (step as any).before('start');
    } catch (e) {
      return Promise.reject(e);
    }
  }
  await process();

  return Promise.resolve();
}

async function previousStep() {
  let futureStep = currentStep.value - 1;

  let process = () =>
    new Promise((resolve, reject) => {
      const cb = steps.value[futureStep].onNextStep;
      if (cb) {
        cb().then(() => {
          currentStep.value = futureStep;
          setTimeout(() => {
            resolve(0);
          }, 300);
        });
      } else {
        currentStep.value = futureStep;
        resolve(0);
      }
    });

  if (futureStep > -1) {
    let step = steps.value[futureStep];
    if ((step as any).before) {
      try {
        await (step as any).before('previous');
      } catch (e) {
        return Promise.reject(e);
      }
    }
    await process();
  }

  return Promise.resolve();
}

async function nextStep() {
  let futureStep = currentStep.value + 1;

  let process = () =>
    new Promise((resolve, _reject) => {
      const cb = steps.value[currentStep.value].onNextStep;
      if (cb) {
        cb().then(() => {
          currentStep.value = futureStep;
          setTimeout(() => {
            resolve(0);
          }, 300);
        });
      } else {
        currentStep.value = futureStep;
        resolve(0);
      }
    });

  if (futureStep < numberOfSteps.value && currentStep.value !== -1) {
    let step = steps.value[futureStep];
    if ((step as any).before) {
      try {
        await (step as any).before('next');
      } catch (e) {
        return Promise.reject(e);
      }
    }
    await process();
  }

  return Promise.resolve();
}

onMounted(() => {
  if (!localStorage.getItem('genlayer.tutorial')) {
    start();
  }
});

onBeforeUnmount(() => {
  if (options.value.useKeyboardNavigation) {
    window.removeEventListener('keyup', handleKeyup);
  }
});

watch(showTutorial, () => {
  if (showTutorial.value) {
    start();
  } else {
    stop();
  }
});
</script>
<template>
  <div class="v-tour bg-slate-300 dark:bg-zinc-700">
    <slot
      :current-step="currentStep"
      :steps="steps"
      :previous-step="previousStep"
      :next-step="nextStep"
      :stop="stop"
      :skip="skip"
      :finish="finish"
      :is-first="isFirst"
      :is-last="isLast"
      :labels="options.labels"
      :enabled-buttons="options.enabledButtons"
      :highlight="options.highlight"
      :debug="options.debug"
    >
      <!--Default slot {{ currentStep }}-->
      <TutorialStep
        v-if="steps[currentStep]"
        :step="steps[currentStep]"
        :key="currentStep"
        :previous-step="previousStep"
        :next-step="nextStep"
        :stop="stop"
        :skip="skip"
        :finish="finish"
        :is-first="isFirst"
        :is-last="isLast"
        :labels="options.labels"
        :enabled-buttons="options.enabledButtons"
        :highlight="options.highlight"
        :stop-on-fail="options.stopOnTargetNotFound"
        :debug="options.debug"
        @targetNotFound="$emit('targetNotFound', $event)"
      >
        <!--<div v-if="index === 2" slot="actions">
            <a @click="nextStep">Next step</a>
          </div>-->
      </TutorialStep>
    </slot>
  </div>
</template>

<style>
body.v-tour--active {
  pointer-events: none;
}

.v-tour {
  pointer-events: auto;
}

.v-tour__target--highlighted {
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.4);
  pointer-events: auto;
  z-index: 9999;
}

.v-tour__target--relative {
  position: relative;
}
</style>
