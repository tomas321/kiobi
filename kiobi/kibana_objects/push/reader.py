#!/usr/bin/env python3

import json

from kiobi.log import log


def read_objects_file(file_fullpath: str):
    with open(file_fullpath, 'r') as fd:
        log.debug("opened '{}' for reading saved objects json".format(file_fullpath))
        return __remove_disallowed_fields(fd.read())


def __remove_disallowed_fields(data: str):
    json_data = json.loads(data)
    for obj in json_data['saved_objects']:
        if 'updated_at' in obj:
            del obj['updated_at']
    return str(json_data)
