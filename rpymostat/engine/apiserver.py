"""
The latest version of this package is available at:
<http://github.com/jantman/RPyMostat>

##################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of RPyMostat, also known as RPyMostat.

    RPyMostat is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RPyMostat is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with RPyMostat.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/RPyMostat> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

from klein import Klein
from twisted.web import server
import logging
import abc  # noqa

from rpymostat.engine.api.v1 import APIv1
from rpymostat.version import VERSION

logger = logging.getLogger(__name__)


class APIServer(object):
    """
    Main class for the Klein-based API server.
    """

    # Note - docs for this are overridden in docs/source/conf.py
    # remove_module_docstring()
    app = Klein()

    def __init__(self, dbconn=None):
        """
        Initialize API Server. Mainly just instantiates the API version classes
        (currently just :py:class:`~.APIv1`) and sets up any global/top-level
        routes.

        Note: it's awful, but ``dbconn`` only has a default value to make
        sphinxcontrib.autohttp happy.

        :param dbconn: MongoDB ConnectionPool
        :type dbconn: txmongo.connection.ConnectionPool
        """
        server.version = 'RPyMostat %s' % VERSION
        # initialize top-level routes first
        self.dbconn = dbconn
        self.app.route('/')(self.handle_root)
        APIv1(self, self.app, dbconn, []).setup_routes()

    def handle_root(self, _self, request):
        """
        root resource (/) request handler. This should only be called by
        the Kelin app as a route.

        This serves the :http:get:`/` endpoint.

        @TODO this should return some helpful information, like the server
        version and a link to the docs, as well as where to obtain the source
        code and a link to the status page.

        :param _self: another reference to ``self``, sent by Klein.
        :param request: the Request
        :type request: instance of :py:class:`twisted.web.server.Request`

        <HTTPAPI>
        Simple informational page that returns HTML describing the program and
        version, where to find the source code, and links to the documentation
        and status page.

        Served by :py:meth:`.handle_root`.

        **Example request**:

        .. sourcecode:: http

          GET / HTTP/1.1
          Host: example.com

        :statuscode 200: no error
        """
        return "Hello, World!"
