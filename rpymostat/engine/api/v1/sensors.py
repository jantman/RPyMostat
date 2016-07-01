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
from rpymostat.db.sensors import update_sensor
from rpymostat.exceptions import RequestParsingException

logger = logging.getLogger(__name__)


class Sensors(SiteHierarchy):
    """
    Manages the v1/sensors portion of the API.
    """

    prefix_part = 'sensors'

    def setup_routes(self):
        """Setup routes for subparts of the hierarchy."""
        self.add_route(self.update, 'update', methods=['POST'])
        # /sensors returns a list
        self.add_route(self.list)

    def list(self, _self, request):
        """
        Handle sensor list API endpoint - return a list of known sensors.

        This serves the :http:get:`/v1/sensors` endpoint.

        :param _self: another reference to ``self`` sent by Klein
        :param request: the Request
        :type request: instance of :class:`twisted.web.server.Request`

        <HTTPAPI>
        Return application status information. Currently just returns the
        text string "Status: Running".

        Served by :py:meth:`.list`.

        **Example request**:

        .. sourcecode:: http

          GET /v1/sensors HTTP/1.1
          Host: example.com

        **Example Response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Type: application/json

          {}

        :statuscode 200: no errors
        """
        return json.dumps({}, sort_keys=True)

    @inlineCallbacks
    def update(self, _self, request):
        """
        Handle updating data from a remote sensor.

        This serves :http:post:`/v1/sensors/update` endpoint.

        @TODO Handle sensor data update.

        :param _self: another reference to ``self`` sent by Klein
        :param request: the Request
        :type request: instance of :class:`twisted.web.server.Request`

        <HTTPAPI>
        Update current data/readings for sensors from a remote RPyMostat-sensor
        device.

        Served by :py:meth:`.update`.

        **Example request**:

        .. sourcecode:: http

          POST /v1/sensors/update HTTP/1.1
          Host: example.com

          {
              'host_id': 'myhostid',
              'sensors': {
                  '1058F50F01080047': {
                     'type': 'DS18S20',
                     'value': 24.3125,
                     'alias': 'some_alias',
                     'extra': 'arbitrary string'
                  },
                  ...
              }
          }

        **Sensor Data Objects**:

        The ``sensors`` request attribute is itself an object (dict/hash). Keys
        are globally-unique sensor IDs. The value is an object with the
        following fields/attributes/keys:

        - **type:** *(string)* descriptive type, such as the sensor model
        - **value:** *(float/decimal or null)* decimal current temperature
          reading in degrees Celsius, or null if the current reading cannot
          be determined.
        - **alias:** *(optional; string)* a human-readable alias or name for
          this sensor, if the system it runs on contains this information. This
          is not to be confused with the name that RPyMostat maintains for the
          sensor.
        - **extra:** *(optional; string)* arbitrary further information about
          this sensor, to be included in details about it.

        **Example Response**:

        .. sourcecode:: http

          HTTP/1.1 202 OK
          Content-Type: application/json

          {"status": "ok", "ids": [ "id_1", "id_2" ]}

        **Example Response**:

        .. sourcecode:: http

          HTTP/1.1 422
          Content-Type: application/json

          {"status": "error", "error": "host_id field is missing"}

        :<json host_id: *(string)* the unique identifier of the sending host
        :<json sensors: *(object)* array of sensor data objects, conforming to
          the description above.
        :>json status: *(string)* the status of the update;
          ``accepted`` or ``done``
        :>json id: *(int)* unique identifier for the update
        :statuscode 201: update has been made in the database
        """
        try:
            data = self._parse_json_request(request)
        except RequestParsingException as ex:
            logger.warning('Exception parsing sensor update request from %s: '
                           '%s', request.client.host, ex.message, exc_info=1)
            request.setResponseCode(400)
            returnValue(
                json.dumps({'status': 'error', 'error': ex.message},
                           sort_keys=True)
            )
        logger.debug('Received sensor update request from %s with content: %s',
                     request.client.host, data)
        request.responseHeaders.addRawHeader(
            b"content-type", b"application/json"
        )
        if 'host_id' not in data:
            request.setResponseCode(422)
            returnValue(json.dumps({
                'status': 'error',
                'error': 'host_id field missing from POST data'
            }, sort_keys=True))
        if 'sensors' not in data:
            request.setResponseCode(422)
            returnValue(json.dumps({
                'status': 'error',
                'error': 'sensors field missing from POST data'
            }, sort_keys=True))
        if not isinstance(data['sensors'], type({})):
            request.setResponseCode(422)
            returnValue(json.dumps({
                'status': 'error',
                'error': 'sensors field must be a JSON object (deserialize to'
                ' a python dict)'
            }, sort_keys=True))
        if len(data['sensors']) < 1:
            request.setResponseCode(422)
            returnValue(json.dumps({
                'status': 'error',
                'error': 'sensors field must not be empty'
            }, sort_keys=True))
        ids = []
        failed = 0
        for sensor_id, sensor_data in data['sensors'].items():
            try:
                _id = yield update_sensor(
                    self.dbconn,
                    data['host_id'],
                    sensor_id,
                    sensor_data['value'],
                    sensor_type=sensor_data.get('type', None),
                    sensor_alias=sensor_data.get('alias', None),
                    extra=sensor_data.get('extra', None)
                )
                logger.debug('update_sensor() return value: %s', _id)
                ids.append(_id)
            except Exception as ex:
                logger.error('Error updating sensor %s: %s', sensor_id,
                             sensor_data, exc_info=1)
                failed += 1
        if failed:
            request.setResponseCode(400)
            if failed == len(data['sensors']):
                returnValue(json.dumps({'status': 'failed'}, sort_keys=True))
            else:
                returnValue(json.dumps({
                    'status': 'partial', 'ids': ids,
                    'error': '%d sensor updates failed' % failed
                }, sort_keys=True))
        request.setResponseCode(201)
        returnValue(json.dumps({'status': 'ok', 'ids': ids}, sort_keys=True))
