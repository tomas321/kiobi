#!/usr/bin/env python3

import json
from os.path import join

from kiobi.log import log

filename = 'saved_objects.json'


def write_objects_to_file(file_fullpath: str, objects: dict):
    log.debug("wirting {} saved objects to '{}'".format(len(list(objects)), join(file_fullpath, filename)))
    with open(join(file_fullpath, filename), 'w') as fd:
        json.dump(objects, fd)
