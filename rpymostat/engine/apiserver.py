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
import logging
import abc

from rpymostat.engine.api.v1 import APIv1

logger = logging.getLogger(__name__)


class APIServer(object):
    """
    Main class for the Klein-based API server.
    """

    # Note - docs for this are overridden in docs/source/conf.py
    app = Klein()

    def __init__(self):
        """
        Initialize API Server. Mainly just instantiates the API version classes
        (currently just :py:class:`~.APIv1`) and sets up any global/top-level
        routes.
        """
        # initialize top-level routes first
        self.app.route('/')(self.handle_root)
        APIv1(self.app, []).setup_routes()

    def handle_root(self, _self, request):
        """
        root resource (/) request handler. This should only be called by
        the Kelin app as a route.

        @TODO this should return some helpful information, like the server
        version and a link to the docs, as well as where to obtain the source
        code and a link to the status page.

        :param _self: another reference to ``self``, sent by Klein.
        :param request: the Request
        :type request: instance of :py:class:`twisted.web.server.Request`
        """
        return "Hello, World!"
