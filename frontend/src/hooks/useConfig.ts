export const useConfig = () => {
  const isHostedEnvironment = import.meta.env.VITE_IS_HOSTED === 'true';
  const canUpdateValidators = !isHostedEnvironment;

  return {
    canUpdateValidators,
  };
};
