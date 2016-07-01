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

import abc  # noqa
import logging
import json

from twisted.internet.defer import inlineCallbacks, returnValue

from rpymostat.engine.site_hierarchy import SiteHierarchy
from rpymostat.db import get_collection, COLL_SENSORS

logger = logging.getLogger(__name__)


class Status(SiteHierarchy):
    """
    Manages the v1/status portion of the API.
    """

    prefix_part = 'status'

    def setup_routes(self):
        """Setup routes for subparts of the hierarchy."""
        self.add_route(self.status)

    @inlineCallbacks
    def status(self, _self, request):
        """
        Report on application and dependency status.

        This serves :http:get:`/v1/status`

        :param _self: another reference to ``self`` sent by Klein
        :param request: the Request
        :type request: instance of :class:`twisted.web.server.Request`

        <HTTPAPI>
        Return application status information (mainly dependent services).

        Served by :py:meth:`.status`.

        **Example request**:

        .. sourcecode:: http

          GET /v1/status HTTP/1.1
          Host: example.com

        **Example Response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Type: application/json

          {
              "status": true,
              "dependencies": {
                  "mongodb": true
              }
          }

        :statuscode 200: operational
        :statuscode 503: non-operational
        """
        status = {'dependencies': {}}
        is_ok = True
        try:
            coll = get_collection(self.dbconn, COLL_SENSORS)
            yield coll.find(limit=1)
            status['dependencies']['mongodb'] = True
        except:
            logger.error('DB connection test failed', exc_info=1)
            status['dependencies']['mongodb'] = False
            is_ok = False
        status['status'] = is_ok
        request.responseHeaders.addRawHeader(
            b"content-type", b"application/json"
        )
        resp = json.dumps(status, sort_keys=True)
        if is_ok:
            request.setResponseCode(200)
        else:
            request.setResponseCode(503)
        returnValue(resp)
