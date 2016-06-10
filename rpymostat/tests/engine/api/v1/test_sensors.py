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

from rpymostat.engine.api.v1.sensors import Sensors
from twisted.web.server import Request

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, MagicMock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, MagicMock, DEFAULT  # noqa

pbm = 'rpymostat.engine.api.v1.sensors'
pb = '%s.Sensors' % pbm


class TestClass(Sensors):

    def __init__(self, app, prefix):
        pass


class TestSensors(object):

    def setup(self):
        self.cls = TestClass(Mock(), [])

    def test_prefix_part(self):
        assert TestClass(Mock(), []).prefix_part == 'sensors'

    def test_setup_routes(self):
        with patch('%s.add_route' % pb, autospec=True) as mock_add_route:
            self.cls.setup_routes()
        assert mock_add_route.mock_calls == [
            call(self.cls, self.cls.update, 'update', methods=['POST']),
            call(self.cls, self.cls.list)
        ]

    def test_list(self):
        assert self.cls.list(self.cls, Mock()) == '{}'

    def test_update(self):
        req_data = {
            'host_id': 'myhostid',
            'sensors': {
                'sensor1': {
                    'type': 's1type',
                    'value': 12.345,
                    'alias': 's1alias',
                    'extra': 'extraS1'
                }
            }
        }
        req_json = json.dumps(req_data)
        mock_req = MagicMock(spec_set=Request)
        mock_req.content.getvalue.return_value = req_json
        type(mock_req).client = Mock(host='myhost')
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            res = self.cls.update(None, mock_req)
        assert res == 'sensor updated.'
        assert mock_req.mock_calls == [
            call.content.getvalue(),
            call.setResponseCode(200)
        ]
        assert mock_logger.mock_calls == [
            call.debug(
                'Received sensor update request from %s with content: %s',
                'myhost',
                req_data
            )
        ]

    def test_update_cant_read_request(self):

        def se_exc():
            raise Exception()

        mock_req = MagicMock(spec_set=Request)
        mock_req.content.getvalue.side_effect = se_exc
        type(mock_req).client = Mock(host='myhost')
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            res = self.cls.update(None, mock_req)
        assert res == 'Could not read request content.'
        assert mock_req.mock_calls == [
            call.content.getvalue(),
            call.setResponseCode(400)
        ]
        assert mock_logger.mock_calls == [
            call.warning('Got sensor update request with no data from %s',
                         'myhost', exc_info=1)
        ]

    def test_update_empty_request(self):
        mock_req = MagicMock(spec_set=Request)
        mock_req.content.getvalue.return_value = ''
        type(mock_req).client = Mock(host='myhost')
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            res = self.cls.update(None, mock_req)
        assert res == 'Empty request.'
        assert mock_req.mock_calls == [
            call.content.getvalue(),
            call.setResponseCode(400)
        ]
        assert mock_logger.mock_calls == [
            call.warning(
                'Got empty sensor update request from: %s', 'myhost'
            )
        ]

    def test_update_not_json(self):
        mock_req = MagicMock(spec_set=Request)
        mock_req.content.getvalue.return_value = 'foo bar'
        type(mock_req).client = Mock(host='myhost')
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            res = self.cls.update(None, mock_req)
        assert res == 'Invalid JSON.'
        assert mock_req.mock_calls == [
            call.content.getvalue(),
            call.setResponseCode(400)
        ]
        assert mock_logger.mock_calls == [
            call.warning(
                'Failed deserializing JSON sensor update request from %s: %s',
                'myhost', 'foo bar', exc_info=1
            )
        ]
