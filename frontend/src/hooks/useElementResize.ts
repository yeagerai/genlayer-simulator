import { watch, ref, onUnmounted, type Ref } from 'vue';

export function useElementResize(el: Ref<HTMLElement | null | undefined>) {
  const width = ref(el?.value?.offsetWidth || 0);
  const height = ref(el?.value?.offsetHeight || 0);
  let ro: ResizeObserver;

  watch(
    () => el?.value,
    () => {
      if (!ro) {
        ro = new ResizeObserver((entries) => {
          for (const entry of entries) {
            width.value = entry.target.clientWidth || 0;
            height.value = entry.target.clientHeight || 0;
          }
        });
        ro.observe(el.value!);
      }
    }
  );
  onUnmounted(() => {
    if (el.value) ro.unobserve(el.value!);
  });

  return { width, height };
}
