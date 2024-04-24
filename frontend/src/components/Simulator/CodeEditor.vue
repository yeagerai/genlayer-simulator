<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api'
import { ref, shallowRef, watch, computed } from 'vue'
import { pythonSyntaxDefinition } from '@/utils'
import { PlayIcon } from '@heroicons/vue/24/solid';
import { useContractsFilesStore, useUIStore } from '@/stores';
import { type ContractFile } from '@/types';


const uiStore = useUIStore()
const contractStore = useContractsFilesStore()
const props = defineProps<{
  contract: ContractFile,
  parentHeight: number,
  parentWidth: number
}>()
const emit = defineEmits(['content-change', 'run-debug'])
const editorElement = ref<HTMLDivElement | null>(null)
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)
const theme = computed(() => uiStore.mode === 'light' ? 'vs' : 'vs-dark')
const editorWidth = ref(0)
const editorHeight = ref(props.parentHeight)

watch(
  () => editorElement.value,
  newValue => {
    if (!editorRef.value && newValue) {
      monaco.languages.register({ id: 'python' })
      monaco.languages.setMonarchTokensProvider('python', pythonSyntaxDefinition)
      editorRef.value = monaco.editor.create(editorElement.value!, {
        value: props.contract.content || '',
        language: 'python',
        theme: theme.value,
        automaticLayout: true,
        formatOnPaste: true,
        formatOnType: true,
      })
      editorRef.value.onDidChangeModelContent(() => {
        contractStore.updateContractFile(props.contract.id!, { content: editorRef.value?.getValue() || "" })
      })
      const height = editorElement.value?.parentNode?.parentElement?.clientHeight || 600
      editorHeight.value = height - 40
      editorWidth.value = editorElement.value?.parentNode?.parentElement?.clientWidth || 950
    }
  },
)

watch(
  () => props.parentHeight,
  () => {
  
      editorHeight.value = editorElement.value?.parentNode?.parentElement?.clientHeight || 600 
  },
)

watch(
  () => props.parentWidth,
  () => {
      editorWidth.value = editorElement.value?.parentNode?.parentElement?.clientWidth || 950
  },
)

watch(
  () => uiStore.mode,
  newValue => {
    if (editorRef.value)
      editorRef.value.updateOptions({ theme: newValue === 'light' ? 'vs' : 'vs-dark' })
  },
)
</script>

<template>
  <div class="flex flex-col">
    <div ref="editorElement" :style="`width: ${editorWidth / 16}rem; height: ${editorHeight / 16}rem`"/>
  </div>
</template>

<style scoped></style>
