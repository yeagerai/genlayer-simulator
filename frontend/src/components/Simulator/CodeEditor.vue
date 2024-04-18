<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api'
import { defineEmits, defineProps, ref, shallowRef, watch, computed } from 'vue'
import { pythonSyntaxDefinition } from '@/utils'
import { PlayIcon } from '@heroicons/vue/24/solid';
import { useContractsFilesStore, useUIStore } from '@/stores';
import { type ContractFile } from '@/types';

const uiStore = useUIStore()
const contractStore = useContractsFilesStore()
const props = defineProps<{
  contract: ContractFile
}>()
const emit = defineEmits(['content-change', 'deploy'])
const editorElement = ref<HTMLDivElement | null>(null)
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)
const theme = computed(() => uiStore.mode === 'light' ? 'vs' : 'vs-dark')
const editorWidth = ref(0)
const editorHeight = ref(0)

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
      editorHeight.value = editorElement.value?.parentNode?.parentElement?.clientHeight || 800
      editorWidth.value = editorElement.value?.parentNode?.parentElement?.clientWidth || 950
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


/**
 * Emits a 'deploy' event with the ID of the contract.
 *
 * @return {void} No return value.
 */
const deployContract = (): void => {
  emit('deploy', props.contract.id)
}
</script>

<template>
  <div class="flex flex-col">
    <div class="flex p-2">
      <button class="flex ml-3" @click="deployContract">
        <PlayIcon class="h-5 w-5 fill-primary" />
        <ToolTip text="Deploy Contract" :options="{ placement: 'bottom' }" />
      </button>
    </div>
    <div ref="editorElement" :style="`width: ${editorWidth / 16}rem; height: ${editorHeight / 16}rem`"/>
  </div>
</template>

<style scoped></style>
