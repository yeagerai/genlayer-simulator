/**
 * Map with a LRU (Least recently used) policy.
 *
 * @link https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU
 */
export class LruMap extends Map {
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
//# sourceMappingURL=lru.js.map