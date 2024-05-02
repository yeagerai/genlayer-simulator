  <script>
  import { DEFAULT_CALLBACKS, DEFAULT_OPTIONS, KEYS } from './constants'
  import TutorialStep from './TutorialStep.vue'
  const steps = [
  {
    target: '.link-contracts',
    header: {
      title: 'This is the title',
    },
    content: 'This is the first step',
  },
  {
    target: '.link-docs',
    content: 'This is the second step, placed on the bottom of the target',
  }
];

  export default {
    components: {
      TutorialStep
    },
    data () {
      return {
        currentStep: -1,
        steps
      }
    },
    mounted () {
      this.start()
    },
    beforeUnmount () {
      // Remove the keyup listener if it has been defined
      if (this.options.useKeyboardNavigation) {
        window.removeEventListener('keyup', this.handleKeyup)
      }
    },
    computed: {
      // Allow us to define custom options and merge them with the default options.
      // Since options is a computed property, it is reactive and can be updated during runtime.
      options () {
        return {
          ...DEFAULT_OPTIONS
        }
      },
      callbacks () {
        return {
          ...DEFAULT_CALLBACKS
        }
      },
      // Return true if the tour is active, which means that there's a VStep displayed
      isRunning () {
        return this.currentStep > -1 && this.currentStep < this.numberOfSteps
      },
      isFirst () {
        return this.currentStep === 0
      },
      isLast () {
        return this.currentStep === this.steps.length - 1
      },
      numberOfSteps () {
        return this.steps.length
      },
      step () {
        return this.steps[this.currentStep]
      }
    },
    methods: {
      async start (startStep) {
        // Register keyup listeners for this tour
        if (this.options.useKeyboardNavigation) {
          window.addEventListener('keyup', this.handleKeyup)
        }
  
        // Wait for the DOM to be loaded, then start the tour
        startStep = typeof startStep !== 'undefined' ? parseInt(startStep, 10) : 0
        let step = this.steps[startStep]
  
        let process = () => new Promise((resolve, reject) => {
          setTimeout(() => {
            this.callbacks.onStart()
            this.currentStep = startStep
            resolve()
          }, this.options.startTimeout)
        })
  
        if (typeof step.before !== 'undefined') {
          try {
            await step.before('start')
          } catch (e) {
            return Promise.reject(e)
          }
        }
        await process()
  
        return Promise.resolve()
      },
      async previousStep () {
        let futureStep = this.currentStep - 1
  
        let process = () => new Promise((resolve, reject) => {
          this.callbacks.onPreviousStep(this.currentStep)
          this.currentStep = futureStep
          resolve()
        })
  
        if (futureStep > -1) {
          let step = this.steps[futureStep]
          if (typeof step.before !== 'undefined') {
            try {
              await step.before('previous')
            } catch (e) {
              return Promise.reject(e)
            }
          }
          await process()
        }
  
        return Promise.resolve()
      },
      async nextStep () {
        let futureStep = this.currentStep + 1
  
        let process = () => new Promise((resolve, reject) => {
          this.callbacks.onNextStep(this.currentStep)
          this.currentStep = futureStep
          resolve()
        })
  
        if (futureStep < this.numberOfSteps && this.currentStep !== -1) {
          let step = this.steps[futureStep]
          if (typeof step.before !== 'undefined') {
            try {
              await step.before('next')
            } catch (e) {
              return Promise.reject(e)
            }
          }
          await process()
        }
  
        return Promise.resolve()
      },
      stop () {
        this.callbacks.onStop()
        document.body.classList.remove('v-tour--active')
        this.currentStep = -1
      },
      skip () {
        this.callbacks.onSkip()
        this.stop()
      },
      finish () {
        this.callbacks.onFinish()
        this.stop()
      },
  
      handleKeyup (e) {
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
      isKeyEnabled (key) {
        const { enabledNavigationKeys } = this.options
        return enabledNavigationKeys[key] ? enabledNavigationKeys[key] : true
      }
    }
  }
  </script>
  <template>
    <div class="v-tour">
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
      box-shadow: 0 0 0 4px rgba(0,0,0,.4);
      pointer-events: auto;
      z-index: 9999;
    }
  
    .v-tour__target--relative {
      position: relative;
    }
  </style>