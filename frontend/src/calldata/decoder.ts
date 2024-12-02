import type { CalldataEncodable } from './types';
import * as consts from './consts';
import { Address } from './types';

function readULeb128(data: Uint8Array, index: { i: number }): bigint {
  let res: bigint = 0n;
  let accum = 0n;
  let shouldContinue = true;
  while (shouldContinue) {
    const byte = data[index.i];
    index.i++;
    const rest = byte & 0x7f;
    res += BigInt(rest) * (1n << accum);
    accum += 7n;
    shouldContinue = byte >= 128;
  }
  return res;
}

function decodeImpl(data: Uint8Array, index: { i: number }): CalldataEncodable {
  const cur = readULeb128(data, index);
  switch (cur) {
    case BigInt(consts.SPECIAL_NULL):
      return null;
    case BigInt(consts.SPECIAL_TRUE):
      return true;
    case BigInt(consts.SPECIAL_FALSE):
      return false;
    case BigInt(consts.SPECIAL_ADDR): {
      const res = data.slice(index.i, index.i + 20);
      index.i += 20;
      return new Address(res);
    }
  }
  const type = Number(cur & 0xffn) & ((1 << consts.BITS_IN_TYPE) - 1);
  const rest = cur >> BigInt(consts.BITS_IN_TYPE);
  switch (type) {
    case consts.TYPE_BYTES: {
      const ret = data.slice(index.i, index.i + Number(rest));
      index.i += Number(rest);
      return ret;
    }
    case consts.TYPE_PINT:
      return rest;
    case consts.TYPE_NINT:
      return -1n - rest;
    case consts.TYPE_STR: {
      const ret = data.slice(index.i, index.i + Number(rest));
      index.i += Number(rest);
      return new TextDecoder('utf-8').decode(ret);
    }
    case consts.TYPE_ARR: {
      const ret = [] as CalldataEncodable[];
      let elems = rest;
      while (elems > 0) {
        elems--;
        ret.push(decodeImpl(data, index));
      }
      return ret;
    }
    case consts.TYPE_MAP: {
      const ret = new Map<string, CalldataEncodable>();
      let elems = rest;
      while (elems > 0) {
        elems--;
        const strLen = Number(readULeb128(data, index));
        const key = data.slice(index.i, index.i + strLen);
        index.i += strLen;
        const keyStr = new TextDecoder('utf-8').decode(key);
        ret.set(keyStr, decodeImpl(data, index));
      }
      return ret;
    }
    default:
      throw new Error(
        `can't decode type from ${type} rest is ${rest} at pos ${index.i}`,
      );
  }
}

export function decode(data: Uint8Array): CalldataEncodable {
  const index = { i: 0 };
  const res = decodeImpl(data, index);
  if (index.i !== data.length) {
    throw new Error('some data left');
  }
  return res;
}
