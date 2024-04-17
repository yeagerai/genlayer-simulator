<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api'
import { defineEmits, defineProps, ref, shallowRef, watch } from 'vue'
import { pythonSyntaxDefinition } from '@/utils'
import { ArrowUpTrayIcon, TrashIcon, PlayIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/solid';

const props = defineProps({
  content: { type: String, default: '' },
})

const emit = defineEmits(['content-change', 'deploy'])

const editorElement = ref(null)
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)
const theme = ref('vs-dark')

watch(
  () => editorElement.value,
  newValue => {
    if (!editorRef.value && newValue) {
      monaco.languages.register({ id: 'python' })
      monaco.languages.setMonarchTokensProvider('python', pythonSyntaxDefinition)
      editorRef.value = monaco.editor.create(editorElement.value!, {
        value: props.content,
        language: 'python',
        theme: theme.value,
        automaticLayout: true,
        formatOnPaste: true,
        formatOnType: true,
      })
    }
  },
)

watch(
  () => props.content,
  newValue => {
    if (editorRef.value && editorRef.value.getValue() !== newValue)
      editorRef.value.setValue(newValue || '')
  },
)

const switchTheme = () => {
  if (theme.value === 'vs-dark')
    theme.value = 'vs'
  else
    theme.value = 'vs-dark'

  editorRef.value?.updateOptions({
    ...editorRef.value.getOptions(),
    theme: theme.value,
  })
}

const clearContent = () => {
  emit('content-change', '')
}

const deployContract = () => {
  emit('deploy')
}

const loadContentFromFile = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const [file] = target.files
    const reader = new FileReader()

    reader.onload = (ev: ProgressEvent<FileReader>) => {
      if (ev.target?.result)
        emit('content-change', (ev.target?.result as string) || '')
    }
    reader.readAsText(file)
  }
}
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="flex p-2">
      <label class="input-label mx-3">
        <div class="flex">
          <ArrowUpTrayIcon class="h-5 w-5 fill-primary" />
          <ToolTip text="Upload File" :options="{ placement: 'bottom' }" />
          <input type="file" @change="loadContentFromFile">
        </div>
      </label>
      <button class="mx-3" @click="deployContract">
        <PlayIcon class="h-5 w-5 fill-primary" />
        <ToolTip text="Deploy Contract" :options="{ placement: 'bottom' }" />
      </button>
      <button class="mx-3" @click="clearContent">
        <TrashIcon class="h-5 w-5 fill-primary" />
        <ToolTip text="Clear Content" :options="{ placement: 'bottom' }" />
      </button>
      <button class="mx-3" @click="switchTheme">
        <SunIcon class="h-5 w-5 fill-primary" v-if="theme === 'vs-dark'" />
        <MoonIcon class="h-5 w-5 fill-primary" v-else />
        <ToolTip text="Swtitch Theme" :options="{ placement: 'bottom' }" />
      </button>
    </div>
    <div ref="editorElement" class="w-full h-full" />
  </div>
</template>

<style scoped>
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
