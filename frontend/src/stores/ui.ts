import { defineStore } from 'pinia';
import type { UIMode, UIState } from '@/types';

export const useUIStore = defineStore('ui', {
  state: (): UIState => {
    return {
      mode: (localStorage.getItem('genLayer.ui-mode') as UIMode) || 'light',
      showTutorial: false,
    };
  },
  actions: {
    toggleMode() {
      if (this.mode === 'light') {
        this.mode = 'dark';
      } else {
        this.mode = 'light';
      }

      this.initialize();
    },
    initialize() {
      localStorage.setItem('genLayer.ui-mode', this.mode);
      document.documentElement.setAttribute('data-mode', this.mode);
    },
    runTutorial() {
      this.showTutorial = true;
    },
  },
});
