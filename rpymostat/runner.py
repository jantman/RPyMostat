"""
Main application entry point / runner for RPyMostat Hub.
"""
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.python import log  # @TODO: see http://twistedmatrix.com/documents/current/core/howto/logging.html and http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging

from rpymostat import settings
from rpymostat.hub.apiserver import HubAPIServer

def run():
    """
    Start running the processes...
    """
    apiserver = HubAPIServer()
    reactor.listenTCP(settings.API_PORT, Site(apiserver.resource))
    reactor.run()

def main():
    """
    Main entry point for running the Hub
    """
    # @TODO: parse args    
    run()
