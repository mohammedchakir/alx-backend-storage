#!/usr/bin/env python3
"""
code for the web.py file implementing the get_page
function with caching and access
"""
import requests
import redis
from functools import wraps


def cache_with_expiry(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cache_key = f"page:{url}"
            count_key = f"count:{url}"

            # Check if the page content is cached
            cached_content = cache.get(cache_key)
            if cached_content:
                # If cached, increment access count
                cache.incr(count_key)
                return cached_content.decode("utf-8")

            # If not cached, fetch the page content
            page_content = func(*args, **kwargs)

            # Cache the page content with an expiration time
            cache.setex(cache_key, seconds, page_content)

            # Initialize access count if not present
            cache.setnx(count_key, 0)
            # Increment access count
            cache.incr(count_key)

            return page_content

        return wrapper

    return decorator


# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)


@cache_with_expiry(10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Connect to Redis
    cache = redis.Redis(host='localhost', port=6379, db=0)

    # Test get_page function
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
