#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""
import uuid
from typing import Union
import redis


class Cache:
    """
    Cache class for storing data in Redis.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache class with a Redis client
        and flushes the Redis instance.
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in
        Redis using the key.
        Args:
            data (Union[str, bytes, int, float]): The data to be
            stored in the cache.
        Returns:
            str: The randomly generated key used for storing the
            data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
