import { ref, onMounted, onUnmounted } from 'vue'

export function useElementResize(el: HTMLDivElement) {
  const width = ref(el.clientWidth)
  const height = ref(el.clientHeight)

  function handler() {
    width.value = el.clientWidth
    height.value = el.clientHeight
  }

  onMounted(() => el.addEventListener('resize', handler))
  onUnmounted(() => el.removeEventListener('resize', handler))

  return { width, height }
}
