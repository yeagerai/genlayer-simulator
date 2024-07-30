import Modal from '@/components/global/Modal.vue';
import Btn from '@/components/global/Btn.vue';

export default function registerGlobalComponents(app) {
  app.component('Modal', Modal);
  app.component('Btn', Btn);
}
