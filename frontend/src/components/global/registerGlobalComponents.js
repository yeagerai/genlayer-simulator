import Modal from '@/components/global/Modal.vue'
import Btn from '@/components/global/Btn.vue'
import GhostBtn from '@/components/global/GhostBtn.vue'
import ConfirmationModal from '@/components/global/ConfirmationModal.vue'

export default function registerGlobalComponents(app) {
  app.component('Modal', Modal)
  app.component('Btn', Btn)
  app.component('GhostBtn', GhostBtn)
  app.component('ConfirmationModal', ConfirmationModal)
}
