#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats():
    """
    Display stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    total_logs = collection.count_documents({})

    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check_count = collection.count_documents({"method": "GET",
                                                     "path": "/status"})
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    log_stats()
