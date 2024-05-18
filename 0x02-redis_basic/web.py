#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""

import redis
import requests
from functools import wraps

r = redis.Redis()


def cache_with_expiry(seconds):
    """Decorator to cache function results with expiration"""
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            """Wrapper function"""
            key = f"cached:{url}"
            count_key = f"count:{url}"
            cached_value = r.get(key)
            if cached_value:
                # If cached value exists, update count and return cached value
                r.incr(count_key, 1)
                return cached_value.decode("utf-8")

            # If not cached, fetch new content
            html_content = func(url)

            # Set cache with expiration time and update count
            r.setex(key, seconds, html_content)
            r.incr(count_key, 1)

            return html_content
        return wrapper
    return decorator


@cache_with_expiry(10)
def get_page(url: str) -> str:
    """Function to obtain the HTML content of a URL"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
