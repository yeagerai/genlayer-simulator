export const BITS_IN_TYPE = 3;

export const TYPE_SPECIAL = 0;
export const TYPE_PINT = 1;
export const TYPE_NINT = 2;
export const TYPE_BYTES = 3;
export const TYPE_STR = 4;
export const TYPE_ARR = 5;
export const TYPE_MAP = 6;

export const SPECIAL_NULL = (0 << BITS_IN_TYPE) | TYPE_SPECIAL;
export const SPECIAL_FALSE = (1 << BITS_IN_TYPE) | TYPE_SPECIAL;
export const SPECIAL_TRUE = (2 << BITS_IN_TYPE) | TYPE_SPECIAL;
export const SPECIAL_ADDR = (3 << BITS_IN_TYPE) | TYPE_SPECIAL;
