#!/usr/bin/env python3

from elasticsearch import Elasticsearch
import json
import requests
import os.path as os_path

from kiobi.log import log


def get_saved_objects(query: dict):
    if 'data' in query and len(query.keys()) != 1:
        raise ValueError("Attempting to call GET request with data")
    return requests.get(**query)


def create_objects(query: dict):
    if 'data' not in query and len(query.keys()) != 2:
        raise ValueError("Missing data in query: {}".format(query))
    response = requests.post(url=query['url'], json=query['data'], headers={'kbn-xsrf': 'true'}).json()

    errors = []
    for obj in response['saved_objects']:
        if 'error' in obj:
            errors.append(obj)
            log.warning("Pushing saved object failed for id '{}'".format(obj['id']))

    return response, errors


def initialize_elasticsearch(es: Elasticsearch, template: str):
    with open(template, 'r') as fd:
        res = es.indices.put_template(name=os_path.splitext(os_path.basename(template))[0], body=json.load(fd))
        if 'error' not in res:
            log.info("Successfully created index template")
        else:
            log.error("Failed to create index template")
            raise ValueError(str(res))
