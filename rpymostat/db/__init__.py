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

from txmongo.connection import ConnectionPool
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

MONGO_DB_NAME = 'rpymostat'


def connect_mongodb(host, port):
    """
    Run :py:func:`~.setup_mongodb`. If that succeeds, connect to MongoDB via
    ``txmongo``. Return a txmongo ConnectionPool.

    :param host: host to connect to MongoDB on.
    :type host: str
    :param port: port to connect to MongoDB on.
    :type port: int
    :return: MongoDB connection pool
    :rtype: txmongo.connection.ConnectionPool
    """
    setup_mongodb(host, port)
    uri = 'mongodb://%s:%d' % (host, port)
    logger.info('Connecting to MongoDB via txmongo at %s', uri)
    try:
        conn = ConnectionPool(uri=uri)
    except:
        logger.critical('Error connecting to MongoDB at %s', uri, exc_info=1)
        raise SystemExit(2)
    return conn


def setup_mongodb(host, port):
    """
    Connect synchronously (outside/before the reactor loop) to MongoDB
    and setup whatever we need. Raise an exception if this fails. This mainly
    exists to test that the DB is running and accessible before running the
    reactor loop.

    :param host: host to connect to MongoDB on.
    :type host: str
    :param port: port to connect to MongoDB on.
    :type port: int
    """
    logger.debug('Connecting to MongoDB via pymongo at %s:%s', host, port)
    try:
        client = MongoClient(host, port, connect=True)
        client.get_database(MONGO_DB_NAME)
    except:
        logger.critical("Error connecting to MongoDB at %s:%s",
                        host, port, exc_info=1)
        raise SystemExit(1)
    logger.debug('PyMongo connection successful.')
