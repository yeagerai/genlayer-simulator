import * as calldata from '@/calldata';
import { AnyFieldValue } from '../global/fields/AnyFieldValue';

export interface SingleArgData {
  val: calldata.CalldataEncodable | AnyFieldValue;
  key: number | string;
}

export interface ArgData {
  args: SingleArgData[];
  kwargs: { [k: string]: SingleArgData };
}

export function unfoldArgsData(args: ArgData): {
  args: calldata.CalldataEncodable[];
  kwargs: { [key: string]: calldata.CalldataEncodable };
} {
  const unfoldOne = (x: SingleArgData) => {
    if (x.val instanceof AnyFieldValue) {
      try {
        return calldata.parse(x.val.value);
      } catch (e) {
        throw new Error(`failed to parse ${x.key}`);
      }
    }
    return x.val;
  };
  return {
    args: args.args.map(unfoldOne),
    kwargs: Object.fromEntries(
      Object.entries(args.kwargs).map(([k, v]) => [k, unfoldOne(v)]),
    ),
  };
}
