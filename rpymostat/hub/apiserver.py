"""
RPyMostat API Hub HTTP server
"""
from klein import Klein
from twisted.python import log
import logging

logger = logging.getLogger(__name__)


class HubAPIServer(object):

    app = Klein()

    def __init__(self):
        pass

    @app.route('/')
    def root(self, request):
        """
        hello world for root resource

        :param request: the Request
        :type request: instance of :class:`twisted.web.server.Request`
        """
        return "Hello, World!"

    @app.route('/<path:path>')
    def catchall(self, request, path):
        logger.debug('Catch-all for path: %s', path)
        return "Got catch-all path '{p}'".format(p=path)
