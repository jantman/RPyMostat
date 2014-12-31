"""
Main application entry point / runner for RPyMostat Hub.
"""
import sys
from twisted.web.server import Site
from twisted.internet import reactor
# @TODO: see http://twistedmatrix.com/documents/current/core/howto/logging.html and http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging
from twisted.python import log

import logging

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)

from rpymostat import settings
from rpymostat.hub.apiserver import HubAPIServer


def run():
    """
    Start running the processes...
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.debug("instantiating apiserver")
    apiserver = HubAPIServer()
    logger.debug("reactor.listenTCP")
    reactor.listenTCP(settings.API_PORT, Site(apiserver.app.resource()))
    logger.debug("rector.run()")
    reactor.run()
    logger.debug("finished")

def main():
    """
    Main entry point for running the Hub
    """
    # @TODO: parse args
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("starting twisted logging")
    log.startLogging(sys.stdout)
    logger.debug("calling run()")
    run()
    logger.debug("run() returned")

if __name__ == "__main__":
    main()
