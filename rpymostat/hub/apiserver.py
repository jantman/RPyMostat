"""
RPyMostat API Hub HTTP server
"""
from klein import Klein
from twisted.python import log


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

    @app.route('/<param>')
    def paramed_url(self, request, param):
        return "Got param '{p}' in argument".format(p=param)
