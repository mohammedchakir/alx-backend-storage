#!/usr/bin/env python3
"""
Function to retrieve schools having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve schools having a specific topic.
    """
    return list(mongo_collection.find({"topics": topic}))
