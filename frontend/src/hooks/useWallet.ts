import { Web3Client } from '@/clients/web3';

export function useWallet() {
  const web3 = new Web3Client();

  function shortenAddress(address?: string) {
    if (!address) {
      return '';
    }

    const maxChars = 4;
    const displayedChars = Math.min(Math.floor(address.length / 3), maxChars);

    return (
      address.slice(0, displayedChars) + '...' + address.slice(-displayedChars)
    );
  }

  return {
    web3,
    shortenAddress,
  };
}
