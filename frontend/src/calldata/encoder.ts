import type { CalldataEncodable } from './types';
import { Address } from './types';

const BITS_IN_TYPE = 3;

const TYPE_SPECIAL = 0;
const TYPE_PINT = 1;
const TYPE_NINT = 2;
const TYPE_BYTES = 3;
const TYPE_STR = 4;
const TYPE_ARR = 5;
const TYPE_MAP = 6;

const SPECIAL_NULL = (0 << BITS_IN_TYPE) | TYPE_SPECIAL;
const SPECIAL_FALSE = (1 << BITS_IN_TYPE) | TYPE_SPECIAL;
const SPECIAL_TRUE = (2 << BITS_IN_TYPE) | TYPE_SPECIAL;
const SPECIAL_ADDR = (3 << BITS_IN_TYPE) | TYPE_SPECIAL;

function reportError(msg: string, data: CalldataEncodable): never {
  throw new Error(`invalid calldata input '${data}'`);
}

function writeNum(to: number[], data: bigint) {
  if (data === 0n) {
    to.push(0);
    return;
  }
  while (data > 0) {
    let cur = Number(data & 0x7fn);
    data >>= 7n;
    if (data > 0) {
      cur |= 0x80;
    }
    to.push(cur);
  }
}

function encodeNumWithType(to: number[], data: bigint, type: number) {
  const res = (data << BigInt(BITS_IN_TYPE)) | BigInt(type);
  writeNum(to, res);
}

function encodeNum(to: number[], data: bigint) {
  if (data >= 0n) {
    encodeNumWithType(to, data, TYPE_PINT);
  } else {
    encodeNumWithType(to, -data - 1n, TYPE_NINT);
  }
}

function compareString(l: number[], r: number[]): number {
  for (let index = 0; index < l.length && index < r.length; index++) {
    const cur = l[index] - r[index];
    if (cur !== 0) {
      return cur;
    }
  }
  return l.length - r.length;
}

function encodeMap(to: number[], arr: Iterable<[string, CalldataEncodable]>) {
  // unicode code points array, utf8 encoded array, item
  const newEntries: [number[], Uint8Array, CalldataEncodable][] = Array.from(
    arr,
    ([k, v]): [number[], Uint8Array, CalldataEncodable] => [
      Array.from(k, (x) => x.codePointAt(0)!),
      new TextEncoder().encode(k),
      v,
    ],
  );
  newEntries.sort((v1, v2) => compareString(v1[0], v2[0]));
  for (let i = 1; i < newEntries.length; i++) {
    if (compareString(newEntries[i - 1][0], newEntries[i][0]) === 0) {
      throw new Error(
        `duplicate key '${new TextDecoder().decode(newEntries[i][1])}'`,
      );
    }
  }

  encodeNumWithType(to, BigInt(newEntries.length), TYPE_MAP);
  for (const [_k, k, v] of newEntries) {
    writeNum(to, BigInt(k.length));
    for (const c of k) {
      to.push(c);
    }
    encodeImpl(to, v);
  }
}

function encodeImpl(to: number[], data: CalldataEncodable) {
  if (data === null || data === undefined) {
    to.push(SPECIAL_NULL);
    return;
  }
  if (data === true) {
    to.push(SPECIAL_TRUE);
    return;
  }
  if (data === false) {
    to.push(SPECIAL_FALSE);
    return;
  }
  switch (typeof data) {
    case 'number': {
      if (!Number.isInteger(data)) {
        reportError('floats are not supported', data);
      }
      encodeNum(to, BigInt(data));
      return;
    }
    case 'bigint': {
      encodeNum(to, data);
      return;
    }
    case 'string': {
      const str = new TextEncoder().encode(data);
      encodeNumWithType(to, BigInt(str.length), TYPE_STR);
      for (const c of str) {
        to.push(c);
      }
      return;
    }
    case 'object': {
      if (data instanceof Uint8Array) {
        encodeNumWithType(to, BigInt(data.length), TYPE_BYTES);
        for (const c of data) {
          to.push(c);
        }
      } else if (data instanceof Array) {
        encodeNumWithType(to, BigInt(data.length), TYPE_ARR);
        for (const c of data) {
          encodeImpl(to, c);
        }
      } else if (data instanceof Map) {
        encodeMap(to, data);
      } else if (data instanceof Address) {
        to.push(SPECIAL_ADDR);
        for (const c of data.bytes) {
          to.push(c);
        }
      } else if (Object.getPrototypeOf(data) === Object.prototype) {
        encodeMap(
          to,
          Object.keys(data).map((k): [string, CalldataEncodable] => [
            k,
            data[k],
          ]),
        );
      } else {
        reportError('unknown object type', data);
      }
      return;
    }
    default:
      reportError('unknown base type', data);
  }
}

export function encode(data: CalldataEncodable): Uint8Array {
  // FIXME: find a better growable type
  const arr: number[] = [];
  encodeImpl(arr, data);
  return new Uint8Array(arr);
}
