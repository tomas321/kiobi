#!/usr/bin/env python3


def retrieve_all_saved_objects_request_uri(host: str, per_page: int = 100, page: int = 1):
    url = "{}/api/saved_objects/_find".format(host)
    types = "type=visualization&type=search&type=index-pattern&type=dashboard"
    # fields = "fields=id&fields=type&fields=title&fields=attributes"
    misc = "per_page={}&page={}".format(per_page, page)

    return {
        "url": "{}?{}&{}".format(url, types, misc)
    }


def retrieve_saved_objects_by_title(host: str, pattern: str, **kwargs):
    url = "{}/api/saved_objects/_find".format(host)
    if 'types' not in kwargs:
        types = "type=visualization&type=search&type=index-pattern&type=dashboard"
    else:
        types = '&'.join(["type={}".format(x) for x in kwargs['types']])
    fields = "search={}&search_fields=title".format(pattern)

    return {
        "url": "{}?{}&{}".format(url, types, fields)
    }


def bulk_create_objects_query(host: str, objects: list):
    url = "{}/api/saved_objects/_bulk_create".format(host)
    data = objects

    return {
        "url": url,
        "data": data
    }
