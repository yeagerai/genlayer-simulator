<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import { ref, shallowRef, watch, defineEmits } from 'vue';
import { rpc } from '@/utils';
const emit = defineEmits(['contract-deployed']);

const editorElement = ref(null)
const content = ref('')
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)

watch(
  () => editorElement.value,
  (newValue) => {
    if (!editorRef.value && newValue) {
      editorRef.value = monaco.editor.create(editorElement.value!, {
        value: content.value,
        language: 'python',
        theme: 'vs-dark',
        automaticLayout: true,
        formatOnPaste: true,
        formatOnType: true
      });
    }
  },
)

watch(
  () => content.value,
  (newValue: string) => {
    if (editorRef.value && editorRef.value.getValue() !== newValue) {
      editorRef.value.setValue(newValue!);
    }
  },
)

const deployContract = async () => {
  console.log('handle contract deply')
  // call json_rpc to get the abi
  // deploy the contract code
 const result = await rpc({
    method: 'deploy_intelligent_contract', 
    params: [
      '0xcAE1bEb0daABFc1eF1f4A1C17be7E7b4cc12B33A',
      content.value,
      '{}'
    ]
  })
  console.log({ result })
}

const clearContent = () => {
  content.value = '';
}

const loadContentFromFile = (event: Event) => {
  const target = (event.target as HTMLInputElement)
  if (target.files && target.files.length > 0) {
    const [file] = target.files;
    const reader = new FileReader();
    reader.onload = (ev: ProgressEvent<FileReader>) => {
      if (ev.target?.result) {
        content.value = ev.target?.result as string || ''
      }
    };
    reader.readAsText(file);
  }
}

</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-spacer></v-spacer>
      <label
        class="input-label v-btn v-btn--icon v-theme--light v-btn--density-default v-btn--size-default v-btn--variant-text">
        <span class="v-btn__overlay"></span>
        <span class="v-btn__underlay"></span>
        <div class="v-btn__content">
          <v-icon>mdi-upload</v-icon>
          <v-tooltip activator="parent" location="bottom">
            Upload File
          </v-tooltip>
          <input type="file" @change="loadContentFromFile">
        </div>
      </label>
      <v-btn icon @click="deployContract" :disabled="content.length < 1">
        <v-icon>mdi-code-greater-than</v-icon>
        <v-tooltip activator="parent" location="bottom">
          Deploy Contract
        </v-tooltip>
      </v-btn>
      <v-btn icon @click="clearContent">
        <v-icon>mdi-arrow-u-left-top</v-icon>
        <v-tooltip activator="parent" location="bottom">
          Restart
        </v-tooltip>
      </v-btn>
    </v-toolbar>
    <div class="editor" ref="editorElement"> </div>
  </v-card>
</template>
<style scoped>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}

.input-label {
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.input-label input {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  opacity: 0;
}
</style>
