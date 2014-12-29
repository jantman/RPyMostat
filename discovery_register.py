#!/usr/bin/env python

""" Example of announcing a service (in this case, a fake HTTP server) """

import socket
import time
from six.moves import input

from zeroconf import ServiceInfo, Zeroconf, InterfaceChoice, DNSOutgoing, _FLAGS_QR_RESPONSE, _FLAGS_AA, _TYPE_PTR, _TYPE_SRV, _CLASS_IN, _TYPE_TXT, _TYPE_A, DNSAddress, DNSText, DNSService, DNSPointer, _REGISTER_TIME, current_time_millis

import logging
FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(name)s%(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()

def register_service(zc, info, ttl=60, send_num=3):
    """
    like zeroconf.Zeroconf.register_service() but
    just broadcasts send_num packets and then returns
    """
    logger.info("Registering service: {s}".format(s=info))
    now = current_time_millis()
    next_time = now
    i = 0
    while i < 3:
        if now < next_time:
            sleep_time = next_time - now
            logger.debug("sleeping {s}".format(s=sleep_time))
            zc.wait(sleep_time)
            now = current_time_millis()
            continue
        out = DNSOutgoing(_FLAGS_QR_RESPONSE | _FLAGS_AA)
        out.add_answer_at_time(DNSPointer(info.type, _TYPE_PTR,
                                          _CLASS_IN, ttl, info.name), 0)
        out.add_answer_at_time(DNSService(info.name, _TYPE_SRV,
                                          _CLASS_IN, ttl, info.priority, info.weight, info.port,
                                          info.server), 0)
        out.add_answer_at_time(DNSText(info.name, _TYPE_TXT, _CLASS_IN,
                                       ttl, info.text), 0)
        if info.address:
            out.add_answer_at_time(DNSAddress(info.server, _TYPE_A,
                                              _CLASS_IN, ttl, info.address), 0)
        zc.send(out)
        i += 1
        next_time += _REGISTER_TIME
    logger.debug("done registering service")

desc = {'path': '/~paulsm/'}

info = ServiceInfo("_http._tcp.local.",
                   "Paul's Test Web Site._http._tcp.local.",
                   socket.inet_aton("10.0.1.2"), 80, 0, 0,
                   desc, "ash-2.local.")

zeroconf = Zeroconf(interfaces=InterfaceChoice.All)
logger.info("Registration of a service...")
try:
    wait_seconds = 60
    while True:
        register_service(zeroconf, info)
        zeroconf.wait(wait_seconds * 1000)
finally:
    logger.info("Unregistering...")
    logger.error("Unregister not implemented")
    zeroconf.close()
    logger.info("Done.")
