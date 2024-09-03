import { v4 as uuidv4 } from 'uuid';

export function useUniqueId(prefix?: string): string {
  const uid = uuidv4();

  if (prefix) {
    return `${prefix}-${uid}`;
  } else {
    return uid;
  }
}
