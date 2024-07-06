<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api'
import { ref, shallowRef, watch, computed, nextTick } from 'vue'
import { pythonSyntaxDefinition } from '@/utils'
import { useContractsStore, useUIStore } from '@/stores';
import { type ContractFile } from '@/types';
import { useElementResize, useWindowResize } from '@/hooks';


const uiStore = useUIStore()
const contractsStore = useContractsStore()
const props = defineProps<{
  contract: ContractFile,
}>()

const editorElement = ref<HTMLDivElement | null>(null)
const containerElement = ref<HTMLElement | null | undefined>(null)
const { width: windowWidth, height: windowHeight } = useWindowResize()
const { width: containerWidth, height: containerHeight } = useElementResize(containerElement)
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)
const theme = computed(() => uiStore.mode === 'light' ? 'vs' : 'vs-dark')
const editorWidth = ref(0)
const editorHeight = ref(0)

const resizeEditor = () => {
  nextTick(() => {
    const height = editorElement.value?.parentNode?.parentElement?.clientHeight || 600
    editorHeight.value = height - 40
    editorWidth.value = editorElement.value?.parentNode?.parentElement?.clientWidth || 950
  })
}
watch(
  () => editorElement.value,
  newValue => {
    if (!editorRef.value && newValue) {
      containerElement.value = editorElement.value?.parentNode?.parentElement
      monaco.languages.register({ id: 'python' })
      monaco.languages.setMonarchTokensProvider('python', pythonSyntaxDefinition)
      editorRef.value = monaco.editor.create(editorElement.value!, {
        value: props.contract.content || '',
        language: 'python',
        theme: theme.value,
        automaticLayout: true,
        renderValidationDecorations: 'on',
        matchBrackets: 'near',
        scrollBeyondLastLine: false,
        useShadowDOM: true,
        lightbulb: {
          enabled: monaco.editor.ShowLightbulbIconMode.On
        },
      
      })

      monaco.editor.setModelMarkers(editorRef.value.getModel()!, "python", [
        {
          startLineNumber: 6,
          startColumn: 0,
          endLineNumber: 6,
          endColumn: 10,
          message: 'TEst Message',
          severity: monaco.MarkerSeverity.Error,
          source: 'python',
          code: 'python'
        }
      ]);
      editorRef.value.onDidChangeModelContent(() => {
        contractsStore.updateContractFile(props.contract.id!, { content: editorRef.value?.getValue() || "" })
      })
      resizeEditor()
    }
  },
)


watch(
  () => uiStore.mode,
  newValue => {
    if (editorRef.value)
      editorRef.value.updateOptions({ theme: newValue === 'light' ? 'vs' : 'vs-dark' })
  },
)
//resize watchers
watch(
  () => windowWidth.value,
  () => {
    resizeEditor()
  },
)
watch(
  () => windowHeight.value,
  () => {
    resizeEditor()
  },
)

watch(
  () => containerWidth.value,
  () => {
    resizeEditor()
  },
)
watch(
  () => containerHeight.value,
  () => {
    resizeEditor()
  },
)
watch(() => contractsStore.currentErrorConstructorInputs, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue) {
    console.log('newValue', newValue)
    const model = editorRef.value?.getModel()
    if (editorRef.value && newValue.lineNumber && model) {

      monaco.editor.setModelMarkers(model, "python", [
        {
          startLineNumber: newValue.lineNumber,
          startColumn: 0,
          endLineNumber: newValue.lineNumber,
          endColumn: 10,
          message: 'TEst Message',
          severity: monaco.MarkerSeverity.Error,
          source: 'owner',
          code: 'owner'
        }
      ]);
    }
  }
})
</script>

<template>
  <div class="flex flex-col">
    <div ref="editorElement" :style="`width: ${editorWidth / 16}rem; height: ${editorHeight / 16}rem`" />
  </div>
</template>

<style scoped></style>
