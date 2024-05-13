import { ref, onMounted, onUnmounted } from 'vue'

export function useElementResize(el: HTMLDivElement) {
  const width = ref(el.offsetWidth)
  const height = ref(el.offsetHeight)

  function handler() {
    console.log('handler', el.offsetWidth, el.clientWidth)
    width.value = el.offsetWidth
    height.value = el.offsetHeight
  }

  onMounted(() => el.addEventListener('resize', handler))
  onUnmounted(() => el.removeEventListener('resize', handler))
  // const ro = new ResizeObserver(entries => {
  //   for (let entry of entries) {
  //     entry.target.style.borderRadius =
  //         Math.max(0, 250 - entry.contentRect.width) + 'px';
  //   }
  // });
  // // Only observe the second box
  // ro.observe(el);

  return { width, height }
}
