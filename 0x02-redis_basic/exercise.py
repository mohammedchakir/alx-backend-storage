#!/usr/bin/env python3
"""Cache class for storing data in Redis."""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count calls and returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and
    outputs for a function in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function for the decorated"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """Displays the history of calls of a particular function."""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    # print(f"{function_name} was called {value} times")
    print("{} was called {} times:".format(function_name, value))
    # inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    # outputs = r.lrange(f"{function_name}:outputs", 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self):
        """
        Initializes the Cache class with a Redis client and
        flushes the Redis instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis
        using the key.
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """get function convert data back to desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Automate the parameterization of Cache.get by integrating the
        appropriate conversion function.
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Parameterize Cache.get automatically by incorporating the suitable
        conversion function.
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("secont")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange(
        "{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange(
        "{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
