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
from rpymostat.db import MONGO_DB_NAME, COLL_SENSORS
from rpymostat.db.sensors import update_sensor
from txmongo.collection import Collection
from rpymostat.tests.support import assert_not_twisted_failure

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'rpymostat.db'


class TestSensors(object):

    def test_update_no_kwargs(self):
        mock_db = Mock(name='mock_db')
        mock_dbconn = Mock(name='mock_dbconn')
        setattr(mock_dbconn, MONGO_DB_NAME, mock_db)
        mock_coll = Mock(spec_set=Collection)
        setattr(mock_db, COLL_SENSORS, mock_coll)
        mock_coll.update.return_value = {
            'updatedExisting': True,
            'connectionId': 1,
            'ok': 1.0,
            'err': None,
            'n': 1
        }
        res = update_sensor(
            mock_dbconn,
            'myhost',
            'mysensor',
            123.45
        )
        data = {
            '_id': 'myhost_mysensor',
            'host_id': 'myhost',
            'sensor_id': 'mysensor',
            'last_reading_C': 123.45
        }
        assert_not_twisted_failure(res.result)
        assert res.result == 'myhost_mysensor'
        assert mock_coll.mock_calls == [
            call.update({'_id': 'myhost_mysensor'}, data, upsert=True,
                        safe=True)
        ]
