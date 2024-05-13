#!/usr/bin/env python3
"""
Function to list all documents in a collection.
"""


def list_all(mongo_collection):
    """
    List all documents in the given MongoDB collection.
    """
    return list(mongo_collection.find())
