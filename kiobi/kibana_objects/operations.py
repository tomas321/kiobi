#!/usr/bin/env python3

from elasticsearch import Elasticsearch
import json
import requests
import os.path as os_path

from kiobi.log import log


def get_saved_objects(query: dict, proxies: dict = None):
    if 'data' in query and len(query.keys()) != 1:
        raise ValueError("Attempting to call GET request with data")
    query['proxies'] = proxies
    return requests.get(**query)


def create_objects(query: dict, proxies: dict = None):
    if 'data' not in query and len(query.keys()) != 2:
        raise ValueError("Missing data in query: {}".format(query))
    response = requests.post(url=query['url'], json=query['data'], headers={'kbn-xsrf': 'true'}, proxies=proxies).json()

    errors = []
    if 'saved_objects' in response:
        for obj in response['saved_objects']:
            if 'error' in obj:
                errors.append(obj)
                log.warning("Pushing saved object failed for id '{}'".format(obj['id']))
    else:
        raise ValueError(response)

    return response, errors


def initialize_elasticsearch(es: Elasticsearch, templates: set):
    for template in templates:
        with open(template, 'r') as fd:
            res = es.indices.put_template(name=os_path.splitext(os_path.basename(template))[0], body=json.load(fd))
            if 'error' not in res:
                log.info("Successfully created index template")
            else:
                raise ValueError("Failed to create index template. msg: {}".format(str(res)))
