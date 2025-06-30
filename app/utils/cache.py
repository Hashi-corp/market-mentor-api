from functools import lru_cache
import time

# Simple in-memory cache with TTL
cache = {}

def get_cache(key):
    """Get a value from the cache if it exists and hasn't expired"""
    if key in cache:
        value, expiry = cache[key]
        if expiry > time.time():
            return value
        else:
            # Remove expired item
            del cache[key]
    return None

def set_cache(key, value, ttl=300):  # Default TTL: 5 minutes
    """Set a value in the cache with a TTL"""
    expiry = time.time() + ttl
    cache[key] = (value, expiry)

def clear_cache():
    """Clear the entire cache"""
    cache.clear()

def remove_expired():
    """Remove all expired items from the cache"""
    now = time.time()
    expired_keys = [k for k, (_, expiry) in cache.items() if expiry <= now]
    for k in expired_keys:
        del cache[k]
