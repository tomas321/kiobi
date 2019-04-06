#!/usr/bin/env python3

import logging

log = logging.getLogger('kiobi')


def setup_logger(lvl):
    if lvl:
        logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s')
        log.setLevel(getattr(logging, lvl))
    else:
        logging.disable(logging.CRITICAL)
