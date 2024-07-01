"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LruMap = void 0;
class LruMap extends Map {
    constructor(size) {
        super();
        Object.defineProperty(this, "maxSize", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: void 0
        });
        this.maxSize = size;
    }
    set(key, value) {
        super.set(key, value);
        if (this.maxSize && this.size > this.maxSize)
            this.delete(this.keys().next().value);
        return this;
    }
}
exports.LruMap = LruMap;
//# sourceMappingURL=lru.js.map