#!/usr/bin/env python3

import argparse
import os

from kiobi.log import setup_logger, log
from kiobi.kibana_objects.push import push_objects, reader
from kiobi.kibana_objects import query


def parse_arguments():
    work_dir = os.path.dirname(os.path.realpath(__file__))
    # caller_dir = os.getcwd()
    #
    # parser = argparse.ArgumentParser(description='Importing and Exporting saved objects')
    # parser.add_argument('-h', '--host', help='Kibana daemon host',
    #                     type=str,
    #                     required=True,
    #                     dest='host')
    # parser.add_argument('-f', '--source_file', help='Path to saved_objects for import',
    #                     type=str,
    #                     required=True,
    #                     dest='file')
    # parser.add_argument('-e', '--es_host', help='Elasticsearch hostname',
    #                     type=str,
    #                     required=True,
    #                     dest='es_host')
    # parser.add_argument('-t', '--es_template', help='Index template file path',
    #                     type=str,
    #                     required=True,
    #                     dest='template')
    # parser.add_argument('-l', '--log_level', help='Script log level',
    #                     type=str,
    #                     required=False,
    #                     default='INFO',
    #                     dest='log_level')
    #
    # arguments = parser.parse_args()
    #
    # settings = {
    #     'query': {
    #         'host': arguments.host
    #     },
    #     'es_host': arguments.es_host,
    #     'template': arguments.template,
    #     'log_level': arguments.log_level,
    #     'file': os.path.join(caller_dir, arguments.file)
    # }

    settings = {
        'query': {
            'host': 'http://elk.bp.local:5601'
        },
        'es_host': 'elk.bp.local',
        'template': os.path.join(work_dir, 'data/es_template.json'),
        'log_level': 'INFO',
        'file': '/home/tomas/Desktop/saved_objects.json' # os.path.join(work_dir, 'data/test_objects.json')
    }

    return settings


def process(preferences):
    data = reader.read_objects_file(preferences['file'])
    request = query.bulk_create_objects_query(preferences['query']['host'], data)
    log.debug("used request: '{}'".format(request))
    with push_objects.ObjectPusher(request, preferences['es_host'], preferences['template']) as pusher:
        pusher.commit_objects()


def main():
    preferences = parse_arguments()
    setup_logger(preferences['log_level'])

    try:
        process(preferences)
    except ValueError as ve:
        log.error("Failed to push objects with '{}': msq: '{}'".format(type(ve).__name__, ve))
    except ConnectionError as ce:
        log.error("Failed to connect to host. msg: '{}'".format(ce))
    except Exception as e:
        log.error("Unexpected error '{}'. msg: '{}'".format(type(e).__name__, e))


if __name__ == '__main__':
    main()
