export class Address {
  bytes: Uint8Array;

  constructor(addr: Uint8Array) {
    if (addr.length != 32) {
      throw new Error(`invalid address length ${addr}`);
    }
    this.bytes = addr;
  }
}

export type CalldataEncodable =
  | null
  | boolean
  | Address
  | number
  | bigint
  | string
  | Uint8Array
  | Address
  | Array<CalldataEncodable>
  | Map<string, CalldataEncodable>
  | { [key: string]: CalldataEncodable };

export type MethodDescription = {
  method: string;
  args: Array<CalldataEncodable>;
};

export type TransactionData = {
  method: string;
  args: CalldataEncodable[];
};
