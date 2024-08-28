export const useShortAddress = () => {
  function shortenAddress(address?: string) {
    if (!address) {
      return '';
    }

    const prefix = address?.startsWith('0x') ? '0x' : '';
    return (
      `${prefix}${address?.replace('0x', '').substring(0, prefix ? 4 : 6)}...${address?.substring(
        (address?.length || 4) - 4,
      )}` || ''
    );
  }

  return {
    shortenAddress,
  };
};
