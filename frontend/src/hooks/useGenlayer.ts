import { simulator } from 'genlayer-js/chains';
import { createClient, createAccount, generatePrivateKey } from 'genlayer-js';

// TODO: update docs: createClient: network -> chain
// TODO: update docs: typo Readding -> Reading
// TODO: update docs: transactionHash as sample string
// TODO: dynamic accounts / keys
// TODO: nonces (deploy/write) ?
// TODO: leader only (deploy/write)? Yes, that is only going to work in the local network

export function useGenlayer() {
  const account = createAccount();
  console.log('account', account);

  const genlayer = createClient({
    chain: simulator,
    account,
  });

  return {
    account,
    genlayer,
  };
}
