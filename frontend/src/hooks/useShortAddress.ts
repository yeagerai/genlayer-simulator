export const useShortAddress = () => {
  function shortenAddress(address?: string) {
    if (!address) {
      return '';
    }

    const displayedChars = Math.min(Math.floor(address.length / 3), 4);

    return (
      address.slice(0, displayedChars) + '...' + address.slice(-displayedChars)
    );
  }

  return {
    shortenAddress,
  };
};
