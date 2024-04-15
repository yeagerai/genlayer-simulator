<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api'
import { defineEmits, defineProps, ref, shallowRef, watch } from 'vue'
import { pythonSyntaxDefinition } from '@/utils'

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
  <VCard>
    <VToolbar density="compact">
      <VSpacer />
      <label class="input-label v-btn v-btn--icon v-theme--light v-btn--density-default v-btn--size-default v-btn--variant-text">
        <span class="v-btn__overlay" />
        <span class="v-btn__underlay" />
        <div class="v-btn__content">
          <VIcon>ri-upload-line</VIcon>
          <VTooltip
            activator="parent"
            location="bottom"
          > Upload File </VTooltip>
          <input
            type="file"
            @change="loadContentFromFile"
          >
        </div>
      </label>
      <VBtn
        icon
        :disabled="props.content.length < 1"
        @click="deployContract"
      >
        <VIcon>ri-play-fill</VIcon>
        <VTooltip
          activator="parent"
          location="bottom"
        >
          Deploy Contract
        </VTooltip>
      </VBtn>
      <VBtn
        icon
        @click="clearContent"
      >
        <VIcon>ri-anticlockwise-2-fill</VIcon>
        <VTooltip
          activator="parent"
          location="bottom"
        >
          Restart
        </VTooltip>
      </VBtn>
      <VBtn
        icon
        @click="switchTheme"
      >
        <VIcon>mdi-theme-light-dark</VIcon>
        <VTooltip
          activator="parent"
          location="bottom"
        >
          Toogle Theme
        </VTooltip>
      </VBtn>
    </VToolbar>
    <div
      ref="editorElement"
      class="editor"
    />
  </VCard>
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
