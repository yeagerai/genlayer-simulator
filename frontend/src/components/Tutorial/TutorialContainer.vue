<script lang="ts">
import { DEFAULT_CALLBACKS, DEFAULT_OPTIONS, KEYS } from './constants'
import TutorialStep from './TutorialStep.vue'
import { useMainStore, useUIStore } from '@/stores';

const steps = [
  {
    target: '#tutorial-welcome',
    header: {
      title: '',
    },
    content: 'Welcome to the genlayer prototype',
    onNextStep: (store: any, router: any) => {
      const file = store.contracts[0]
      if (file) {
        store.openFile(file.id)
      }
    },
  },
  {
    target: '#tutorial-contract-0',
    content: 'Here is the code editor',
    onNextStep: (store: any, router: any) => {
      router.push({ name: 'simulator.run-debug', query: { deployCurrent: true } })
    },
  },
  {
    target: '#tutorial-how-to-deploy',
    content: 'Here\'s how to deploy',
    onNextStep: (store: any, router: any) => {
      router.push({ name: 'simulator.run-debug', query: { deployCurrent: true } })
    },
  },
  {
    target: '#tutorial-how-to-create-transaction',
    content: 'Here\'s how to create a transaction',
  },
  {
    target: '#tutorial-node-output',
    content: 'Here is the node output as it\'s executing the tx',
  },

  {
    target: '#tutorial-contract-state',
    content: 'Here is the the contract state',
  },
  {
    target: '#tutorial-tx-response',
    content: 'Here is the tx response',
    onNextStep: (store: any, router: any) => {
      router.push({ name: 'simulator.contracts' })
    },
  },
  {
    target: '#tutorial-how-to-change-example',
    content: 'Here\'s how to change to another example',
  }
];

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
  mounted() {
    if (!localStorage.getItem('genlayer.tutorial')) {
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
      const store = useMainStore()
      store.setCurrentContractId('')
      // Register keyup listeners for this tour
      if (this.options.useKeyboardNavigation) {
        window.addEventListener('keyup', this.handleKeyup)
      }

      // Wait for the DOM to be loaded, then start the tour
      startStep = startStep ? parseInt(`${startStep}`, 10) : 0
      let step = this.steps[startStep]

      let process = () => new Promise((resolve, _reject) => {
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

      let process = () => new Promise((resolve, reject) => {
        this.callbacks.onPreviousStep(this.currentStep)
        const cb = this.steps[futureStep].onNextStep
        if (cb) {
          cb(useMainStore(), this.$router)
        }
        this.currentStep = futureStep
        resolve(0)
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

      let process = () => new Promise((resolve, _reject) => {
        this.callbacks.onNextStep(this.currentStep)
        const cb = this.steps[this.currentStep].onNextStep
        if (cb) {
          cb(useMainStore(), this.$router)
        }
        this.currentStep = futureStep
        resolve(0)
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
  <div class="v-tour">
    <slot :current-step="currentStep" :steps="steps" :previous-step="previousStep" :next-step="nextStep" :stop="stop"
      :skip="skip" :finish="finish" :is-first="isFirst" :is-last="isLast" :labels="options.labels"
      :enabled-buttons="options.enabledButtons" :highlight="options.highlight" :debug="options.debug">
      <!--Default slot {{ currentStep }}-->
      <TutorialStep v-if="steps[currentStep]" :step="steps[currentStep]" :key="currentStep"
        :previous-step="previousStep" :next-step="nextStep" :stop="stop" :skip="skip" :finish="finish"
        :is-first="isFirst" :is-last="isLast" :labels="options.labels" :enabled-buttons="options.enabledButtons"
        :highlight="options.highlight" :stop-on-fail="options.stopOnTargetNotFound" :debug="options.debug"
        @targetNotFound="$emit('targetNotFound', $event)">
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
  box-shadow: 0 0 0 4px rgba(0, 0, 0, .4);
  pointer-events: auto;
  z-index: 9999;
}

.v-tour__target--relative {
  position: relative;
}
</style>