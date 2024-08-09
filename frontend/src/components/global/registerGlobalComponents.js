import Modal from '@/components/global/Modal.vue';
import Btn from '@/components/global/Btn.vue';
import GhostBtn from '@/components/global/GhostBtn.vue';
import ConfirmationModal from '@/components/global/ConfirmationModal.vue';
import CopyTextButton from '@/components/global/CopyTextButton.vue';
import Alert from '@/components/global/Alert.vue';
import Loader from '@/components/global/Loader.vue';
import EmptyListPlaceholder from '@/components/global/EmptyListPlaceholder.vue';

export const globalComponents = {
  Modal,
  Btn,
  GhostBtn,
  ConfirmationModal,
  CopyTextButton,
  Alert,
  Loader,
  EmptyListPlaceholder,
};

export function registerGlobalComponents(app) {
  Object.keys(globalComponents).forEach((key) => {
    app.component(key, globalComponents[key]);
  });
}
