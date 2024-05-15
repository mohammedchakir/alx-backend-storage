#!/usr/bin/env python3
"""
code for the web.py file implementing the get_page
function with caching and access
"""
import requests
import redis
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

            # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    # Connect to Redis
    cache = redis.Redis(host='localhost', port=6379, db=0)

    # Test get_page function
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
