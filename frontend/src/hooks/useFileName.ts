export const useFileName = () => {
  function cleanupFileName(name: string) {
    const tokens = name.split('.');
    if (tokens.length > 0) {
      return `${tokens[0]}.gpy`;
    }
    return `${name}.gpy`;
  }

  return {
    cleanupFileName,
  };
};
