<script lang="ts">
import { rpcClient } from '@/utils'
import { DEFAULT_CALLBACKS, DEFAULT_OPTIONS, KEYS } from './constants'
import TutorialStep from './TutorialStep.vue'
import { useMainStore, useUIStore } from '@/stores'
import { notify } from '@kyvg/vue3-notification'

const loadExample = async (mainStore: any) => {
  if (mainStore.contracts.find((c: any) => c.id === 'tutorial-example')) return
  const contractsBlob = import.meta.glob('./wizard_of_coin.py', {
    query: '?raw',
    import: 'default'
  })
  const raw = await contractsBlob['./wizard_of_coin.py']()
  const contract = {
    id: 'tutorial-example',
    name: 'ExampleContract.py',
    content: ((raw as string) || '').trim()
  }
  mainStore.addContractFile(contract)
}

const steps = [
  {
    target: '#tutorial-welcome',
    header: {
      title: 'Welcome to GenLayer Simulator!'
    },
    content: 'This tutorial will guide you through the basics. Click “Next” to begin!',
    onNextStep: async (store: any) => {
      store.openFile('tutorial-example')
    }
  },
  {
    target: '#tutorial-contract-example',
    header: {
      title: 'Code Editor'
    },
    content: "Write and edit your Intelligent Contracts here. The example contract 'ExampleContract.py' is preloaded for you.",
    onNextStep: async (store: any, router: any) => {
      router.push({ name: 'simulator.run-debug', query: { tutorial: true } })
    }
  },
  {
    target: '#tutorial-how-to-deploy',
    header: {
      title: 'Deploying Contracts'
    },
    content: "Click “Next” to automatically deploy your Intelligent Contract to the GenLayer network.",
    onNextStep: async (store: any, router: any) => {
      const contract = store.contracts.find((c: any) => c.id === 'tutorial-example')
      const { result } = await rpcClient.call({
        method: 'deploy_intelligent_contract',
        params: [
          store.currentUserAddress,
          'WizardOfCoin',
          contract.content,
          `{ "have_coin": "True" }`
        ]
      })

      if (result?.status === 'success') {
        store.addDeployedContract({
          address: result?.data.contract_id,
          contractId: contract.id,
          defaultState: `{ "have_coin": "True" }`
        })
        notify({
          title: 'OK',
          text: 'Contract deployed',
          type: 'success'
        })
      } else {
        notify({
          title: 'Error',
          text:
            typeof result.message === 'string' ? result.message : 'Error Deploying the contract',
          type: 'error'
        })
      }
    }
  },
  {
    target: '#tutorial-node-output',
    header: {
      title: 'Node Output'
    },
    content: "View real-time feedback as your transaction execution and debug any issues."
  },

  {
    target: '#tutorial-contract-state',
    header: {
      title: 'Contract State'
    },
    content: "This panel shows the contract's data after executing transactions."
  },
  {
    target: '#tutorial-tx-response',
    header: {
      title: 'Transaction Response'
    },
    content: 'See the results of your transaction interaction with the contract in this area.',
    onNextStep: async (store: any, router: any) => {
      router.push({ name: 'simulator.contracts' })
    }
  },
  {
    header: {
      title: 'Switching Examples'
    },
    target: '#tutorial-how-to-change-example',
    content: "Switch between different example contracts to explore various features and functionalities.",
    onNextStep: async (store: any, router: any) => {
      await router.push({ name: 'simulator.settings' })
    }
  },
  {
    header: {
      title: 'Validators'
    },
    target: '#tutorial-validators',
    content: "Configure the number of validators and set up their parameters here."
  },
  {
    header: {
      title: 'Congratulations!'
    },
    target: '#tutorial-end',
    content: "You've completed the GenLayer Simulator tutorial. Feel free to revisit any step or start experimenting with your own contracts. Happy coding!"
  }
]

export default {
  components: {
    TutorialStep
  },
  data() {
    return {
      currentStep: -1,
      steps
    }
  },
  async mounted() {
    const store = useMainStore()
    if (!localStorage.getItem('genlayer.tutorial')) {
      await loadExample(store)
      localStorage.setItem('genlayer.tutorial', new Date().getTime().toString())
      this.start()
    }
  },
  beforeUnmount() {
    // Remove the keyup listener if it has been defined
    if (this.options.useKeyboardNavigation) {
      window.removeEventListener('keyup', this.handleKeyup)
    }
  },
  computed: {
    // Allow us to define custom options and merge them with the default options.
    // Since options is a computed property, it is reactive and can be updated during runtime.
    options() {
      return {
        ...DEFAULT_OPTIONS
      }
    },
    callbacks() {
      return {
        ...DEFAULT_CALLBACKS
      }
    },
    // Return true if the tour is active, which means that there's a VStep displayed
    isRunning() {
      return this.currentStep > -1 && this.currentStep < this.numberOfSteps
    },
    isFirst() {
      return this.currentStep === 0
    },
    isLast() {
      return this.currentStep === this.steps.length - 1
    },
    numberOfSteps() {
      return this.steps.length
    },
    step() {
      return this.steps[this.currentStep]
    },
    showTutorial() {
      const uiStore = useUIStore()
      return uiStore.showTutorial
    }
  },
  methods: {
    async start(startStep?: number) {
      this.$router.replace({ name: 'simulator.contracts' })
      const store = useMainStore()
      store.openFile('tutorial-example')
      store.setCurrentContractId('')
      // Register keyup listeners for this tour
      if (this.options.useKeyboardNavigation) {
        window.addEventListener('keyup', this.handleKeyup)
      }

      // Wait for the DOM to be loaded, then start the tour
      startStep = startStep ? parseInt(`${startStep}`, 10) : 0
      let step = this.steps[startStep]

      let process = () =>
        new Promise((resolve, _reject) => {
          setTimeout(() => {
            this.callbacks.onStart()
            this.currentStep = startStep
            resolve(0)
          }, this.options.startTimeout)
        })

      if ((step as any).before) {
        try {
          await (step as any).before('start')
        } catch (e) {
          return Promise.reject(e)
        }
      }
      await process()

      return Promise.resolve()
    },
    async previousStep() {
      let futureStep = this.currentStep - 1

      let process = () =>
        new Promise((resolve, reject) => {
          this.callbacks.onPreviousStep(this.currentStep)
          const cb = this.steps[futureStep].onNextStep
          if (cb) {
            cb(useMainStore(), this.$router).then(() => {
              this.currentStep = futureStep
              setTimeout(() => {
                resolve(0)
              }, 300);
            })
          } else {
            this.currentStep = futureStep
            resolve(0)
          }
        })

      if (futureStep > -1) {
        let step = this.steps[futureStep]
        if ((step as any).before) {
          try {
            await (step as any).before('previous')
          } catch (e) {
            return Promise.reject(e)
          }
        }
        await process()
      }

      return Promise.resolve()
    },
    async nextStep() {
      let futureStep = this.currentStep + 1

      let process = () =>
        new Promise((resolve, _reject) => {
          this.callbacks.onNextStep(this.currentStep)
          const cb = this.steps[this.currentStep].onNextStep
          if (cb) {
            cb(useMainStore(), this.$router).then(() => {
              this.currentStep = futureStep
              setTimeout(() => {
                resolve(0)
              }, 300);
            })
          } else {
            this.currentStep = futureStep
            resolve(0)
          }
        })

      if (futureStep < this.numberOfSteps && this.currentStep !== -1) {
        let step = this.steps[futureStep]
        if ((step as any).before) {
          try {
            await (step as any).before('next')
          } catch (e) {
            return Promise.reject(e)
          }
        }
        await process()
      }

      return Promise.resolve()
    },
    stop() {
      this.callbacks.onStop()
      document.body.classList.remove('v-tour--active')
      this.currentStep = -1
    },
    skip() {
      this.callbacks.onSkip()
      this.stop()
    },
    finish() {
      this.callbacks.onFinish()
      this.stop()
    },

    handleKeyup(e: KeyboardEvent) {
      if (this.options.debug) {
        console.log('[Vue Tour] A keyup event occured:', e)
      }
      switch (e.keyCode) {
        case KEYS.ARROW_RIGHT:
          this.isKeyEnabled('arrowRight') && this.nextStep()
          break
        case KEYS.ARROW_LEFT:
          this.isKeyEnabled('arrowLeft') && this.previousStep()
          break
        case KEYS.ESCAPE:
          this.isKeyEnabled('escape') && this.stop()
          break
      }
    },
    isKeyEnabled(key: 'escape' | 'arrowRight' | 'arrowLeft'): boolean {
      if (this.options.enabledNavigationKeys && this.options.enabledNavigationKeys[key]) {
        return this.options.enabledNavigationKeys[key]
      }
      return false
    }
  },
  watch: {
    showTutorial() {
      if (this.showTutorial) {
        this.start()
      } else {
        this.stop()
      }
    }
  }
}
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
