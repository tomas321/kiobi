#!/usr/bin/env python3

from kiobi.log import log
import kiobi.kibana_objects.operations as operations

host = 'elk.bp.local:5601'
find_api = 'api/saved_objects/_find?'


class ObjectPuller:
    def __init__(self, query: dict, proxies: dict = None):
        self.__query = query
        self.__proxies = proxies

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def retrieve_objects(self):
        response = operations.get_saved_objects(self.__query, self.__proxies).json()
        log.debug("Retrieved {} saved objects".format(response['total']))
        if response['total']:
            return response['saved_objects']
