import VTour from '@/components/Tutorial/TutorialComponent.vue'
import VStep from '@/components/Tutorial/TutorialStep.vue'
import type { App } from 'vue'

export const tutorialPlugin = {
  install (app: App<Element>) {
    app.component(VTour.name!, VTour)
    app.component(VStep.name!, VStep)

    // Object containing Tour objects (see VTour.vue) where the tour name is used as key
    app.config.globalProperties.$tours = {}
  }
}
