#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """

import socket

from six.moves import input

from zeroconf import ServiceBrowser, Zeroconf, InterfaceChoice

import logging
FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()

class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        logger.info("Service removed: {n}".format(n=name))

    def add_service(self, zeroconf, type, name):
        logger.info("Service added: '%s' (type is %s)", name, type)
        info = zeroconf.get_service_info(type, name)
        if info:
            logger.debug("'{name}' service info: {info}".format(name=name, info=info))
        else:
            logger.debug("Service has no info")

if __name__ == '__main__':
    zeroconf = Zeroconf(interfaces=InterfaceChoice.All)
    logger.info("Browsing services...")
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    try:
        input("Waiting (press Enter to exit)...\n\n")
    finally:
        zeroconf.close()
    logger.info("Done.")
