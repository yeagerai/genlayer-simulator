import type { CalldataEncodable } from './types';
import { Address } from './types';
import * as consts from './consts';

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
  const res = (data << BigInt(consts.BITS_IN_TYPE)) | BigInt(type);
  writeNum(to, res);
}

function encodeNum(to: number[], data: bigint) {
  if (data >= 0n) {
    encodeNumWithType(to, data, consts.TYPE_PINT);
  } else {
    encodeNumWithType(to, -data - 1n, consts.TYPE_NINT);
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

  encodeNumWithType(to, BigInt(newEntries.length), consts.TYPE_MAP);
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
    to.push(consts.SPECIAL_NULL);
    return;
  }
  if (data === true) {
    to.push(consts.SPECIAL_TRUE);
    return;
  }
  if (data === false) {
    to.push(consts.SPECIAL_FALSE);
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
      encodeNumWithType(to, BigInt(str.length), consts.TYPE_STR);
      for (const c of str) {
        to.push(c);
      }
      return;
    }
    case 'object': {
      if (data instanceof Uint8Array) {
        encodeNumWithType(to, BigInt(data.length), consts.TYPE_BYTES);
        for (const c of data) {
          to.push(c);
        }
      } else if (data instanceof Array) {
        encodeNumWithType(to, BigInt(data.length), consts.TYPE_ARR);
        for (const c of data) {
          encodeImpl(to, c);
        }
      } else if (data instanceof Map) {
        encodeMap(to, data);
      } else if (data instanceof Address) {
        to.push(consts.SPECIAL_ADDR);
        for (const c of data.bytes) {
          to.push(c);
        }
      } else if (Object.getPrototypeOf(data) === Object.prototype) {
        encodeMap(to, Object.entries(data));
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

function toStringImplMap(
  data: Iterable<[string, CalldataEncodable]>,
  to: string[],
) {
  to.push('{');
  for (const [k, v] of data) {
    to.push(JSON.stringify(k));
    to.push(':');
    toStringImpl(v, to);
  }
  to.push('}');
}

function toStringImpl(data: CalldataEncodable, to: string[]) {
  if (data === null || data === undefined) {
    to.push('null');
    return;
  }
  if (data === true) {
    to.push('true');
    return;
  }
  if (data === false) {
    to.push('false');
    return;
  }
  switch (typeof data) {
    case 'number': {
      if (!Number.isInteger(data)) {
        reportError('floats are not supported', data);
      }
      to.push(data.toString());
      return;
    }
    case 'bigint': {
      to.push(data.toString());
      return;
    }
    case 'string': {
      to.push(JSON.stringify(data));
      return;
    }
    case 'object': {
      if (data instanceof Uint8Array) {
        to.push('b#');
        for (const b of data) {
          to.push(b.toString(16));
        }
      } else if (data instanceof Array) {
        to.push('[');
        for (const c of data) {
          toStringImpl(c, to);
          to.push(',');
        }
        to.push(']');
      } else if (data instanceof Map) {
        toStringImplMap(data.entries(), to);
      } else if (data instanceof Address) {
        to.push('addr#');
        for (const c of data.bytes) {
          to.push(c.toString(16));
        }
      } else if (Object.getPrototypeOf(data) === Object.prototype) {
        toStringImplMap(Object.entries(data), to);
      } else {
        reportError('unknown object type', data);
      }
      return;
    }
    default:
      reportError('unknown base type', data);
  }
}

export function toString(data: CalldataEncodable): string {
  const to: string[] = [];
  toStringImpl(data, to);
  return to.join('');
}
