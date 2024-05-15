#!/usr/bin/env python3
"""
code for the web.py file implementing the get_page
function with caching and access
"""
import requests
import redis
from functools import wraps
from typing import Callable

redis = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator guy """
        redis.incr(f"count:{url}")
        cached_response = redis.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        redis.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """get page self descriptive
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
