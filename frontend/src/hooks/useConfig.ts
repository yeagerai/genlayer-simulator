import { ref, computed } from 'vue';

export const useConfig = () => {
  const isLocalNetwork = ref(window.location.hostname === 'localhost');

  const canUpdateValidators = computed(() => isLocalNetwork.value);

  return {
    canUpdateValidators,
  };
};
