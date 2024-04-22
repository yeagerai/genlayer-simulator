import { defineStore } from 'pinia'
import type { UIMode, UIState } from '@/types'

export const useUIStore = defineStore('ui', {
  state: (): UIState => {
    return {
      mode: (localStorage.getItem('ui-mode') as UIMode) || 'light'
    }
  },
  actions: {
    toogleMode() {
      if (this.mode === 'light') {
        this.mode = 'dark'
      } else {
        this.mode = 'light'
      }

      this.initialize()
    },
    initialize() {
      localStorage.setItem('ui-mode', this.mode)
    }
  }
})
