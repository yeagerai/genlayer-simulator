import Modal from '@/components/global/Modal.vue';
import Btn from '@/components/global/Btn.vue';
import GhostBtn from '@/components/global/GhostBtn.vue';
import ConfirmationModal from '@/components/global/ConfirmationModal.vue';
import Alert from '@/components/global/Alert.vue';
import Loader from '@/components/global/Loader.vue';

export default function registerGlobalComponents(app) {
  app.component('Modal', Modal);
  app.component('Btn', Btn);
  app.component('GhostBtn', GhostBtn);
  app.component('ConfirmationModal', ConfirmationModal);
  app.component('Alert', Alert);
  app.component('Loader', Loader);
}
