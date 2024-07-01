import { BaseError } from './base.js';
export type SliceOffsetOutOfBoundsErrorType = SliceOffsetOutOfBoundsError & {
    name: 'SliceOffsetOutOfBoundsError';
};
export declare class SliceOffsetOutOfBoundsError extends BaseError {
    name: string;
    constructor({ offset, position, size, }: {
        offset: number;
        position: 'start' | 'end';
        size: number;
    });
}
export type SizeExceedsPaddingSizeErrorType = SizeExceedsPaddingSizeError & {
    name: 'SizeExceedsPaddingSizeError';
};
export declare class SizeExceedsPaddingSizeError extends BaseError {
    name: string;
    constructor({ size, targetSize, type, }: {
        size: number;
        targetSize: number;
        type: 'hex' | 'bytes';
    });
}
export type InvalidBytesLengthErrorType = InvalidBytesLengthError & {
    name: 'InvalidBytesLengthError';
};
export declare class InvalidBytesLengthError extends BaseError {
    name: string;
    constructor({ size, targetSize, type, }: {
        size: number;
        targetSize: number;
        type: 'hex' | 'bytes';
    });
}
//# sourceMappingURL=data.d.ts.map