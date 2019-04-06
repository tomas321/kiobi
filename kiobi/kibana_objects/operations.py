#!/usr/bin/env python3

import requests


def get_saved_objects(query: dict):
    if 'data' in query and len(query.keys()) != 1:
        raise ValueError("Attempting to call GET request with data")
    return requests.get(**query)


def create_objects(query: dict):
    if 'data' not in query and len(query.keys()) != 2:
        raise ValueError("Missing data in query: {}".format(query))
    return requests.post(**query)
