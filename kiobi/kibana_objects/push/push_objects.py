#!/usr/bin/env python3

import elasticsearch

from kiobi.log import log
import kiobi.kibana_objects.operations as operations


class ObjectPusher:
    def __init__(self, query: dict, es_host: str, template_path: str):
        self.__query = query
        self.__es = elasticsearch.Elasticsearch(hosts=[{"host": es_host, "port": 9200}])
        self.__template_path = template_path

    def __enter__(self):
        operations.initialize_elasticsearch(self.__es, self.__template_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit_objects(self):
        response, failed = operations.create_objects(self.__query)

        log.debug("response message: {}".format(response))
        log.info('Attempted to create {} object(s) and {} failed'.format(len(response['saved_objects']), len(failed)))
