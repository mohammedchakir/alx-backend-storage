#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient
from collections import Counter


def log_stats():
    """
    Display stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check_count = logs_collection.count_documents({"method": "GET",
                                                          "path": "/status"})
    print("{} status check".format(status_check_count))

    ip_counts = Counter(log['ip'] for log in logs_collection.find())
    top_ips = ip_counts.most_common(10)
    print("IPs:")
    for ip, count in top_ips:
        print("\t{}: {}".format(ip, count))


if __name__ == "__main__":
    log_stats()
