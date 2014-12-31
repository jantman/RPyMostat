"""
RPyMostat API Hub HTTP server
"""
from klein import Klein


class HubAPIServer(Object):

    def __init__(self):
        app = Klein()

    @app.route('/')
    def root(self, request):
        """ hello world for root resource """
        return "Hello, World!"

    @property
    def resource(self):
        return self.app.resource()
