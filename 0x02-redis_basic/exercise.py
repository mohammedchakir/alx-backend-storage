#!/usr/bin/env python3
"""Cache class for storing data in Redis."""

import uuid
from typing import Union, Callable
import redis
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        # Append input arguments to the Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the original method to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in the Redis list
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self) -> None:
        """Initializes the Cache class with a Redis client and flushes the Redis instance."""
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()


    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis using the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in the cache.

        Returns:
            str: The randomly generated key used for storing the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("secont")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
