#!/usr/bin/env python3
"""
Function to insert a new document into a collection based on kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the given MongoDB collection
    based on the provided kwargs.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
