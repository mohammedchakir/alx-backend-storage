#!/usr/bin/env python3
"""
Module to insert a new document in a collection based on kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into a MongoDB collection based on kwargs.
    """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id
