import './assets/main.css';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Notifications from '@kyvg/vue3-notification';
import App from './App.vue';
import router from './router';
import { persistStorePlugin, TransactionsListenerPlugin } from '@/plugins';
import { RpcClient, setupStores } from '@/utils';
import { JsonRpcService } from './services/JsonRpcService';
import { VueSpinnersPlugin } from 'vue3-spinners';
import { createGtm } from '@gtm-support/vue-gtm';
import registerGlobalComponents from '@/components/global/registerGlobalComponents';
import { VueQueryPlugin } from '@tanstack/vue-query';
import FloatingVue from 'floating-vue';
import 'floating-vue/dist/style.css';

const app = createApp(App);
const pinia = createPinia();

pinia.use(persistStorePlugin);
app.use(pinia);
app.use(VueQueryPlugin);
app.use(router);
app.use(FloatingVue, {
  themes: {
    tooltip: {
      delay: {
        show: 0,
        hide: 0,
      },
    },
  },
});
app.use(Notifications);
app.provide('$jsonRpc', new JsonRpcService(new RpcClient()));
app.use(VueSpinnersPlugin);
app.use(TransactionsListenerPlugin, {
  interval: 5000,
});

app.use(
  createGtm({
    id: import.meta.env.VITE_GTM_ID,
    enabled: import.meta.env.mode === 'production',
    debug: false,
    vueRouter: router,
  }),
);

registerGlobalComponents(app);

app.mount('#app');
setupStores();
