#!/usr/bin/env python3
"""Cache class for storing data in Redis."""

import uuid
from typing import Union, Callable
import redis
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method of the Cache class is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self) -> None:
        """Initializes the Cache class with a Redis client and flushes the Redis instance."""
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()


    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis using the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis using the given key and optionally
        applies a conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data


if __name__ == "__main__":
    cache = Cache()

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))
