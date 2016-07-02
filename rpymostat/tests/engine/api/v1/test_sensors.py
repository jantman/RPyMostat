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
import pytest

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
        self.dbconn = Mock()


class TestSensors(object):

    def setup(self):
        self.cls = TestClass(Mock(), [])

    def test_prefix_part(self):
        assert TestClass(Mock(), []).prefix_part == 'sensors'

    def test_setup_routes(self):
        with patch('%s.add_route' % pb, autospec=True) as mock_add_route:
            self.cls.setup_routes()
        assert mock_add_route.mock_calls == [
            call(self.cls, self.cls.update, 'update', methods=['PUT']),
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
        type(mock_req).responseHeaders = Mock()
        mock_req.content.getvalue.return_value = req_json
        type(mock_req).client = Mock(host='myhost')
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch('%s._parse_json_request' % pb) as mock_parse:
                with patch('%s.update_sensor' % pbm, autospec=True) as mock_upd:
                    mock_upd.return_value = 'myid'
                    mock_parse.return_value = req_data
                    res = self.cls.update(None, mock_req)
        assert res.result == '{"ids": ["myid"], "status": "ok"}'
        assert mock_parse.mock_calls == [call(mock_req)]
        assert mock_req.mock_calls == [call.setResponseCode(201)]
        assert mock_logger.mock_calls == [
            call.debug(
                'Received sensor update request from %s with content: %s',
                'myhost',
                req_data
            ),
            call.debug('update_sensor() return value: %s', 'myid')
        ]

    @pytest.mark.integration
    def test_integration_update(self, docker_mongodb):
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
        type(mock_req).responseHeaders = Mock()
        mock_req.content.getvalue.return_value = req_json
        type(mock_req).client = Mock(host='myhost')
        """
        @TODO - integration test - set the current value in Mongo,
        send a request, check the response and the new Mongo value.
        """
