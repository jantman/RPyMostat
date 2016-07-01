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
import pytest
from freezegun import freeze_time
from freezegun.api import FakeDatetime

from rpymostat.db import (
    MONGO_DB_NAME, connect_mongodb, setup_mongodb, get_collection
)

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


class TestDBInit(object):

    def test_connect(self):
        with patch.multiple(
            pbm,
            autospec=True,
            logger=DEFAULT,
            setup_mongodb=DEFAULT,
            ConnectionPool=DEFAULT,
        ) as mocks:
            res = connect_mongodb('myhost', 1234)
        assert mocks['setup_mongodb'].mock_calls == [call('myhost', 1234)]
        assert mocks['ConnectionPool'].mock_calls == [
            call(uri='mongodb://myhost:1234')
        ]
        assert mocks['logger'].mock_calls == [
            call.info('Connecting to MongoDB via txmongo at %s',
                      'mongodb://myhost:1234')
        ]
        assert res == mocks['ConnectionPool'].return_value

    def test_connect_exception(self):

        def se_exc(*args, **kwargs):
            raise Exception('foo')

        with patch.multiple(
            pbm,
            autospec=True,
            logger=DEFAULT,
            setup_mongodb=DEFAULT,
            ConnectionPool=DEFAULT,
        ) as mocks:
            mocks['ConnectionPool'].side_effect = se_exc
            with pytest.raises(SystemExit) as excinfo:
                connect_mongodb('myhost', 1234)
        assert excinfo.value.code == 2
        assert mocks['setup_mongodb'].mock_calls == [call('myhost', 1234)]
        assert mocks['ConnectionPool'].mock_calls == [
            call(uri='mongodb://myhost:1234')
        ]
        assert mocks['logger'].mock_calls == [
            call.info('Connecting to MongoDB via txmongo at %s',
                      'mongodb://myhost:1234'),
            call.critical('Error connecting to MongoDB at %s',
                          'mongodb://myhost:1234', exc_info=1)
        ]

    @freeze_time('2015-01-10 12:13:14')
    def test_setup_mongodb(self):
        with patch('%s.MongoClient' % pbm, autospec=True) as mock_client:
            with patch('%s.logger' % pbm, autospec=True) as mock_logger:
                setup_mongodb('h', 12)
        assert mock_client.mock_calls == [
            call('h', 12, connect=True, connectTimeoutMS=5000,
                 serverSelectionTimeoutMS=5000, socketTimeoutMS=5000,
                 waitQueueTimeoutMS=5000),
            call().get_database(MONGO_DB_NAME),
            call().get_database().get_collection('dbtest'),
            call().get_database().get_collection().update(
                {'_id': 'setup_mongodb'},
                {'dt': FakeDatetime(2015, 1, 10, 12, 13, 14),
                 '_id': 'setup_mongodb'
                 },
                j=True,
                upsert=True,
                w=1
            ),
            call().close()
        ]
        assert mock_logger.mock_calls == [
            call.debug('Connecting to MongoDB via pymongo at %s:%s',
                       'h', 12),
            call.info('Connected to MongoDB via pymongo at %s:%s',
                      'h', 12),
            call.debug('Trying a DB upsert'),
            call.debug('MongoDB write completed successfully.')
        ]

    def test_setup_mongodb_exception(self):

        def se_exc(*args, **kwargs):
            raise Exception('foo')

        with patch('%s.MongoClient' % pbm, autospec=True) as mock_client:
            with patch('%s.logger' % pbm, autospec=True) as mock_logger:
                mock_client.side_effect = se_exc
                with pytest.raises(SystemExit) as excinfo:
                    setup_mongodb('h', 12)
        assert excinfo.value.code == 1
        assert mock_client.mock_calls == [
            call('h', 12, connect=True, connectTimeoutMS=5000,
                 serverSelectionTimeoutMS=5000, socketTimeoutMS=5000,
                 waitQueueTimeoutMS=5000)
        ]
        assert mock_logger.mock_calls == [
            call.debug('Connecting to MongoDB via pymongo at %s:%s',
                       'h', 12),
            call.critical('Error connecting to MongoDB at %s:%s',
                          'h', 12, exc_info=1)
        ]

    def test_get_collection(self):
        mock_coll = Mock()
        mock_db = Mock(foo=mock_coll)
        mock_conn = Mock(rpymostat=mock_db)
        assert get_collection(mock_conn, 'foo') == mock_coll
