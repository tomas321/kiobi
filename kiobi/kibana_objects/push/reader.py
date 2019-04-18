#!/usr/bin/env python3

import json

from kiobi.log import log


def read_objects_file(file_fullpath: str):
    with open(file_fullpath, 'r') as fd:
        log.debug("opened '{}' for reading saved objects json".format(file_fullpath))
        return fd.read()
