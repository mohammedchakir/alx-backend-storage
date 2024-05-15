#!/usr/bin/env python3
"""
This function fetches the HTML content
of a URL using the requests module
"""
import requests
import redis
from functools import wraps


def cache_with_expiry(seconds):
    """decorator for get_page function"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper function"""
            url = args[0]
            cache_key = f"page:{url}"
            count_key = f"count:{url}"
            cached_content = cache.get(cache_key)
            if cached_content:
                cache.incr(count_key)
                return cached_content.decode("utf-8")
            page_content = func(*args, **kwargs)
            cache.setex(cache_key, seconds, page_content)
            cache.setnx(count_key, 0)
            cache.incr(count_key)
            return page_content
        return wrapper
    return decorator


@cache_with_expiry(10)
def get_page(url: str) -> str:
    """get function"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    cache = redis.Redis(host='localhost', port=6379, db=0)
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
