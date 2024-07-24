import type { App } from 'vue';
import { defu } from 'defu';
import { hideAll } from 'tippy.js';
import { defineAsyncComponent } from 'vue';
import type { Props } from 'tippy.js';
export const tooltipOptionsInject = Symbol();
type PluginOptions = Partial<Props>;

export function createToolTipPlugin(options: PluginOptions) {
  return (app: App) => {
    options = defu(options, {
      arrow: false,
    });

    app.config.globalProperties.$hideAllTooltips = hideAll;

    app.provide(tooltipOptionsInject, options);
    app.component(
      'ToolTip',
      defineAsyncComponent(() => import('./ToolTip.vue'))
    );
  };
}
