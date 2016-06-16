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
import sys
import json

from rpymostat.engine.api.v1.status import Status
from twisted.web.server import Request
from txmongo.collection import Collection
from rpymostat.db import COLL_SENSORS

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'rpymostat.engine.api.v1.status'
pb = '%s.Status' % pbm


class TestClass(Status):

    def __init__(self, apiserver, app, dbconn, prefix):
        pass


class TestStatus(object):

    def test_prefix_part(self):
        assert TestClass(Mock(), Mock(), Mock(), []).prefix_part == 'status'

    def test_setup_routes(self):
        cls = TestClass(Mock(), Mock(), Mock(), [])
        with patch('%s.add_route' % pb, autospec=True) as mock_add_route:
            cls.setup_routes()
        assert mock_add_route.mock_calls == [
            call(cls, cls.status)
        ]

    def test_status(self):
        mock_req = Mock(spec_set=Request)
        mock_headers = Mock()
        type(mock_req).responseHeaders = mock_headers
        mock_coll = Mock(spec_set=Collection)
        mock_coll.find.return_value = []
        mock_dbconn = Mock()
        cls = TestClass(Mock(), Mock(), mock_dbconn, [])
        cls.dbconn = mock_dbconn
        with patch('%s.get_collection' % pbm, autospec=True) as mock_get_coll:
            with patch('%s.returnValue' % pbm) as mock_retval:
                with patch('%s.logger' % pbm, autospec=True) as mock_logger:
                    mock_get_coll.return_value = mock_coll
                    cls.status(cls, mock_req)
        expected = json.dumps({
            'status': True,
            'dependencies': {'mongodb': True}
        })
        assert mock_headers.mock_calls == [
            call.addRawHeader(
                b"content-type", b"application/json")
        ]
        assert mock_coll.mock_calls == [call.find(limit=1)]
        assert mock_req.mock_calls == [call.setResponseCode(200)]
        assert mock_get_coll.mock_calls == [call(mock_dbconn, COLL_SENSORS)]
        # need to mock out get_collection and the find method on its result
        # also mock the request object and assert on calls
        assert mock_retval.mock_calls == [
            call(expected)
        ]
        assert mock_logger.mock_calls == []

    def test_status_mongo_fail(self):

        def se_exc(**kwargs):
            raise Exception()

        mock_req = Mock(spec_set=Request)
        mock_headers = Mock()
        type(mock_req).responseHeaders = mock_headers
        mock_coll = Mock(spec_set=Collection)
        mock_coll.find.side_effect = se_exc
        mock_dbconn = Mock()
        cls = TestClass(Mock(), Mock(), mock_dbconn, [])
        cls.dbconn = mock_dbconn
        with patch('%s.get_collection' % pbm, autospec=True) as mock_get_coll:
            with patch('%s.returnValue' % pbm) as mock_retval:
                with patch('%s.logger' % pbm, autospec=True) as mock_logger:
                    mock_get_coll.return_value = mock_coll
                    cls.status(cls, mock_req)
        expected = json.dumps({
            'status': False,
            'dependencies': {'mongodb': False}
        })
        assert mock_headers.mock_calls == [
            call.addRawHeader(
                b"content-type", b"application/json")
        ]
        assert mock_coll.mock_calls == [call.find(limit=1)]
        assert mock_req.mock_calls == [call.setResponseCode(503)]
        assert mock_get_coll.mock_calls == [call(mock_dbconn, COLL_SENSORS)]
        # need to mock out get_collection and the find method on its result
        # also mock the request object and assert on calls
        assert mock_retval.mock_calls == [
            call(expected)
        ]
        assert mock_logger.mock_calls == [
            call.error('DB connection test failed', exc_info=1)
        ]
