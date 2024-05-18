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
                cache.incr(count_key, 1)
                cache.expire(cache_key, seconds)
                return cached_content.decode("utf-8")
            page_content = func(*args, **kwargs)
            cache.set(cache_key, page_content)
            cache.expire(cache_key, seconds)
            cache.incr(count_key, 1)
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
