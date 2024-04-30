<script setup lang="ts">
import { getCurrentInstance, h, onMounted } from 'vue';
const app = getCurrentInstance()
const $tours: any = app?.appContext.config.globalProperties.$tours;
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

onMounted(() => {
  console.log('$tours', $tours)
  $tours?.simulatorTour?.start();
})
</script>
<template>
  <v-tour name="simulatorTour" :steps="steps">
    <template v-slot="tour">
      <transition name="fade">
        <v-step v-if="tour.steps[tour.currentStep]" :key="tour.currentStep" :step="tour.steps[tour.currentStep]"
          :previous-step="tour.previousStep" :next-step="tour.nextStep" :stop="tour.stop" :skip="tour.skip"
          :is-first="tour.isFirst" :is-last="tour.isLast" :labels="tour.labels">

          <template #header v-if="tour.steps[tour.currentStep].header?.title">
            {{ tour.steps[tour.currentStep].header?.title }}
          </template>
          <template #content>
            {{ tour.steps[tour.currentStep].content }}
          </template>
          <template v-if="tour.currentStep === 2" #actions>
            <div>
              <button @click="tour.previousStep" class="btn btn-primary">Previous step 1</button>
              <button @click="tour.nextStep" class="btn btn-primary">Next step</button>
            </div>
          </template>
        </v-step>
      </transition>
    </template>
  </v-tour>
</template>
<style>
.v-tour {
  background-color: rgba(0, 0, 0, 50%);
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 888;
}
</style>