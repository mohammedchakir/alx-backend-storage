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
            with r.pipeline() as pipe:
                while True:
                    try:
                        pipe.watch(key)
                        cached_value = pipe.get(key)
                        if cached_value:
                            pipe.multi()
                            pipe.incr(count_key, 1)
                            pipe.expire(key, seconds)
                            pipe.execute()
                            return cached_value.decode("utf-8")

                        # If not cached, fetch new content
                        html_content = func(url)

                        # Set cache with expiration time and update count
                        pipe.multi()
                        pipe.setex(key, seconds, html_content)
                        pipe.incr(count_key, 1)
                        pipe.execute()

                        return html_content
                    except redis.WatchError:
                        continue
                    finally:
                        pipe.reset()
        return wrapper
    return decorator


@cache_with_expiry(10)
def get_page(url: str) -> str:
    """Function to obtain the HTML content of a URL"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
