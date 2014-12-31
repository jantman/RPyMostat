"""
RPyMostat API Hub HTTP server
"""
from klein import Klein

    
class HubAPIServer(object):

    app = Klein()
    
    def __init__(self):
        pass

    @app.route('/')
    def root(self, request):
        """ hello world for root resource """
        return "Hello, World!"

    @app.route('/<param>')
    def paramed_url(self, request, param):
        return "Got param '{p}' in argument".format(p=param)
    
