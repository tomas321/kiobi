#!/usr/bin/env python3

import argparse
import os

from kiobi.log import setup_logger, log
from kiobi.kibana_objects.pull import pull_objects, writer
from kiobi.kibana_objects import query


def parse_arguments():
    caller_dir = os.getcwd()

    parser = argparse.ArgumentParser(description='Importing and Exporting saved objects')
    parser.add_argument('-H', '--host', help='Kibana daemon host',
                        type=str,
                        required=True,
                        dest='host')
    parser.add_argument('--http_proxy', help='HTTP proxy',
                        type=str,
                        required=False,
                        default=None,
                        dest='http_proxy')
    parser.add_argument('--https_proxy', help='HTTPS proxy',
                        type=str,
                        required=False,
                        default=None,
                        dest='https_proxy')
    parser.add_argument('-l', '--log_level', help='Script log level',
                        type=str,
                        required=False,
                        default='INFO',
                        dest='log_level')
    parser.add_argument('-d', '--dest_path', help='Path for saved_objects location',
                        type=str,
                        required=False,
                        default=caller_dir,
                        dest='path')
    parser.add_argument('-s', '--size', help="Number of saved objects to retrieve. Equivalent to 'per_page' API option",
                        type=int,
                        required=False,
                        default=100,
                        dest='size')
    parser.add_argument('-o', '--offset', help="Nth page from retrieved objects. Equivalent to 'page' API option",
                        type=int,
                        required=False,
                        default=1,
                        dest='offset')

    arguments = parser.parse_args()

    settings = {
        'query': {
            'host': arguments.host,
            'page': arguments.offset,
            'per_page': arguments.size
        },
        'log_level': arguments.log_level,
        'path': arguments.path,
        'proxies': {}
    }

    if arguments.http_proxy:
        settings['proxies']['http'] = arguments.http_proxy
    if arguments.https_proxy:
        settings['proxies']['https'] = arguments.https_proxy

    # settings = {
    #     'query': {
    #         'host': 'http://elk.bp.local:5601',
    #         'page': 1,
    #         'per_page': 100
    #     },
    #     'log_level': 'DEBUG',
    #     'path': '/tmp'
    # }

    return settings


def process(preferences):
    request = query.retrieve_all_saved_objects_request_uri(**preferences['query'])
    log.debug("HTTP request: '{}'".format(request['url']))
    with pull_objects.ObjectPuller(request, preferences['proxies']) as puller:
        data = puller.retrieve_objects()
        writer.write_objects_to_file(preferences['path'], data)


def main():
    preferences = parse_arguments()
    setup_logger(preferences['log_level'])

    try:
        process(preferences)
    except ValueError as ve:
        log.error("Failed to pull objects with '{}': msq: '{}'".format(type(ve).__name__, ve))
    except ConnectionError as ce:
        log.error("Failed to connect to host. msg: '{}'".format(ce))
    except Exception as e:
        log.error("Unexpected error '{}'. msg: '{}'".format(type(e).__name__, e))


if __name__ == '__main__':
    main()
