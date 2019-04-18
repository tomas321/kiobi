#!/usr/bin/env python3

import elasticsearch

from kiobi.log import log
import kiobi.kibana_objects.operations as operations


class ObjectPusher:
    def __init__(self, query: dict, es_host: str = None, template_paths: set = None, proxies: dict = None):
        self.__query = query
        self.__es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": 9200}]) if es_host else None
        self.__template_paths = template_paths
        self.__proxies = proxies

    def __enter__(self):
        if self.__es:
            operations.initialize_elasticsearch(self.__es, self.__template_paths)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit_objects(self):
        response, failed = operations.create_objects(self.__query, self.__proxies)

        log.debug("response message: {}".format(response))
        log.info('Attempted to create {} object(s) and {} failed'.format(len(response['saved_objects']), len(failed)))
