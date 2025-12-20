import threading

class CacheService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CacheService, cls).__new__(cls)
                cls._instance._cache = {}
        return cls._instance

    def get(self, key):
        """Retrieve a value from the cache."""
        return self._cache.get(key)

    def set(self, key, value):
        """Set a value in the cache."""
        with self._lock:
            # Basic cache eviction (simple limit)
            if len(self._cache) > 1000:
                self._cache.pop(next(iter(self._cache)))
            self._cache[key] = value

    def clear(self):
        """Clear the cache."""
        with self._lock:
            self._cache.clear()

# Global instance
cache_service = CacheService()
