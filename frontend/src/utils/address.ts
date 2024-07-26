export function shortenAddress(address?: string) {
  const prefix = address?.startsWith('0x') ? '0x' : '';
  return (
    `${prefix}${address?.replace('0x', '').substring(0, prefix ? 4 : 6)}...${address?.substring(
      (address?.length || 4) - 4,
    )}` || ''
  );
}
