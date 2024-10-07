import { describe, it, expect } from 'vitest';

import * as calldata from '@/calldata';

describe('calldata parsing tests', () => {
  it('string escapes', () => {
    expect(calldata.parse('"\\n"')).toEqual('\n');
    expect(calldata.parse('"\\r"')).toEqual('\r');
    expect(calldata.parse('"\\t"')).toEqual('\t');
    expect(calldata.parse('"\\u00029e3d"')).toEqual('𩸽');
  });
  it('numbers', () => {
    expect(calldata.parse('0')).toEqual(0n);
    expect(calldata.parse('0xff')).toEqual(0xffn);
    expect(calldata.parse('0o77')).toEqual(0o77n);
  });

  it('numbers + sign', () => {
    expect(calldata.parse('+0')).toEqual(0n);
    expect(calldata.parse('+0xff')).toEqual(0xffn);
    expect(calldata.parse('+0o77')).toEqual(0o77n);
  });

  it('numbers - sign', () => {
    expect(calldata.parse('-0')).toEqual(-0n);
    expect(calldata.parse('-0xff')).toEqual(-0xffn);
    expect(calldata.parse('-0o77')).toEqual(-0o77n);
  });

  it('all types', () => {
    const asStr = `{
            'true': true,
            'false': false,
            'null': null,
            str: '123',
            str2: "abc",
            num: 0xf,
            bytes: b#dead,
            addr: addr#0000000000000000000000000000000000000000000000000000000000000000,
            arr: [-2, -0o7, -0xff00, -0]
        }`;
    const asLiteral = {
      true: true,
      false: false,
      null: null,
      str: '123',
      str2: 'abc',
      num: 0xf,
      bytes: new Uint8Array([0xde, 0xad]),
      addr: new calldata.Address(new Uint8Array(new Array(32).map(() => 0))),
      arr: [-2, -0o7, -0xff00, -0],
    };

    expect(calldata.encode(calldata.parse(asStr))).toEqual(
      calldata.encode(asLiteral),
    );
  });

  it('trailing comma', () => {
    const asStr = `
        {
            a: {},
            b: {x: 2,},
            c: [],
            d: [1,],
        }`;
    const asLit = {
      a: {},
      b: { x: 2 },
      c: [],
      d: [1],
    };
    expect(calldata.encode(calldata.parse(asStr))).toEqual(
      calldata.encode(asLit),
    );
  });
});
