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

import logging

from rpymostat.db import COLL_SENSORS, get_collection
from twisted.internet.defer import inlineCallbacks, returnValue

logger = logging.getLogger(__name__)


@inlineCallbacks
def update_sensor(dbconn, host_id, sensor_id, value, sensor_type=None,
                  sensor_alias=None, extra=None):
    """
    Update data for a single sensor in the database.

    :param dbconn: MongoDB database connection
    :type dbconn: txmongo.connection.ConnectionPool
    :param host_id: host_id that the sensor is reporting from
    :type host_id: str
    :param sensor_id: unique sensor ID
    :type sensor_id: str
    :param value: sensor reading in degress Celsius
    :type value: float
    :param sensor_type: description of the type of sensor
    :type sensor_type: str
    :param sensor_alias: human-readable alias for the sensor
    :type sensor_alias: str
    :param extra: extra information about the sensor
    :type extra: str
    :return: database record ID
    :rtype: str
    """
    _id = '%s_%s' % (host_id, sensor_id)
    data = {'_id': _id, 'host_id': host_id, 'sensor_id': sensor_id,
            'last_reading_C': value}
    if sensor_type is not None:
        data['type'] = sensor_type
    if sensor_alias is not None:
        data['alias'] = sensor_alias
    if extra is not None:
        data['extra'] = extra
    logger.debug('Updating sensor %s: %s', _id, data)
    coll = get_collection(dbconn, COLL_SENSORS)
    res = yield coll.replace_one(
        {"_id": _id},
        data,
        upsert=True
    )
    logger.debug('Update result for %s: %s (%s)', _id, res, vars(res))
    returnValue(_id)
