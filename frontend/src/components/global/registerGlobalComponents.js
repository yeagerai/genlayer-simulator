import Modal from '@/components/global/Modal.vue';
import Btn from '@/components/global/Btn.vue';
import GhostBtn from '@/components/global/GhostBtn.vue';
import ConfirmationModal from '@/components/global/ConfirmationModal.vue';
import SelectField from '@/components/global/SelectField.vue';
import NumberField from '@/components/global/NumberField.vue';
import FieldLabel from '@/components/global/FieldLabel.vue';
import TextAreaField from '@/components/global/TextAreaField.vue';
import FieldError from '@/components/global/FieldError.vue';

export default function registerGlobalComponents(app) {
  app.component('Modal', Modal);
  app.component('Btn', Btn);
  app.component('GhostBtn', GhostBtn);
  app.component('ConfirmationModal', ConfirmationModal);
  app.component('SelectField', SelectField);
  app.component('NumberField', NumberField);
  app.component('FieldLabel', FieldLabel);
  app.component('TextAreaField', TextAreaField);
  app.component('FieldError', FieldError);
}
