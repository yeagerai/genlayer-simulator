<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import { ref, shallowRef, watch, computed, onMounted } from 'vue';
import { useContractsStore, useUIStore } from '@/stores';
import { type ContractFile } from '@/types';
import pythonSyntax from '@/constants/pythonSyntax';

const uiStore = useUIStore();
const contractStore = useContractsStore();
const props = defineProps<{
  contract: ContractFile;
}>();

const editorElement = ref<HTMLDivElement | null>(null);
const containerElement = ref<HTMLElement | null | undefined>(null);
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null);
const theme = computed(() => (uiStore.mode === 'light' ? 'vs' : 'vs-dark'));

function initEditor() {
  containerElement.value = editorElement.value?.parentElement;
  monaco.languages.register({ id: 'python' });
  monaco.languages.setMonarchTokensProvider('python', pythonSyntax);
  editorRef.value = monaco.editor.create(editorElement.value!, {
    value: props.contract.content || '',
    language: 'python',
    theme: theme.value,
    automaticLayout: true,
    formatOnPaste: true,
    formatOnType: true,
  });
  editorRef.value.onDidChangeModelContent(() => {
    contractStore.updateContractFile(props.contract.id!, {
      content: editorRef.value?.getValue() || '',
      updatedAt: new Date().toISOString(),
    });
  });
}

onMounted(() => {
  initEditor();
});

watch(
  () => uiStore.mode,
  (newValue) => {
    if (editorRef.value)
      editorRef.value.updateOptions({
        theme: newValue === 'light' ? 'vs' : 'vs-dark',
      });
  },
);
</script>

<template>
  <div ref="editorElement" class="h-full w-full"></div>
</template>
