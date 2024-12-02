import { describe, it, expect } from 'vitest';

import * as calldata from '@/calldata';

describe('calldata decoding tests', () => {
  it('smoke', () => {
    const bin_b64 =
      'DgF4PQAQCBgBAQEBAQEBAQEBAQEBAQEBAQEBAcwB0YDRg9GB0YHQutC40LUg0LHRg9C60LLRi1FK';
    const bin_text =
      'eyd4JzpbbnVsbCx0cnVlLGZhbHNlLGFkZHIjMDEwMTAxMDEwMTAxMDEwMTAxMDEwMTAxMDEwMTAxMDEwMTAxMDEwMSwn0YDRg9GB0YHQutC40LUg0LHRg9C60LLRiycsMTAsLTEwLF0sfQ==';

    const bin = Uint8Array.from(atob(bin_b64), (c) => c.charCodeAt(0));

    const text_decoded_to_arr = Uint8Array.from(atob(bin_text), (c) =>
      c.charCodeAt(0),
    );
    const text = new TextDecoder('utf-8').decode(text_decoded_to_arr);

    const parsed = calldata.parse(text);
    const decoded = calldata.decode(bin);
    expect(decoded).toEqual(parsed);
  });
});
