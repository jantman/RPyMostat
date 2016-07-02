"""
RPyMostat test support / fixtures

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

import os
from subprocess import Popen, PIPE
from signal import SIGINT
from retrying import retry
import requests
import json


def assert_resp_code(r, code):
    """
    Assert about a response code, with a helpful message.
    :param r: response
    :type r: requests.models.Response
    :param code: expected response code
    :type code: int
    """
    msg = "Expected status code to be %s but got %s\n%s" % (
        code, r.status_code, response_info(r)
    )
    assert r.status_code == code, msg


def assert_resp_json(r, d):
    """
    Assert about a response JSON content, with a helpful message.

    :param r: response
    :type r: requests.models.Response
    :param d: json dict
    :type d: dict
    """
    try:
        raw = r.json()
        j = json.dumps(
            raw, sort_keys=True, indent=4, separators=(',', ':')
        )
    except:
        j = raw = r.content
    msg = "Expected response JSON of:\n%s\nBut got:\n%s\n%s" % (
        json.dumps(d, sort_keys=True, indent=4, separators=(',', ':')),
        j, response_info(r)
    )
    assert raw == d, msg


def response_info(r):
    """
    Provide a string of information about a HTTP response, for use in assertion
    messages.

    :param r: response
    :type r: requests.models.Response
    """
    s = "HTTP %s %s from: %s (in %s)\n" % (
        r.status_code, r.reason, r.url, r.elapsed
    )
    s += "Headers:\n"
    for k in sorted(r.headers.keys()):
        s += "\t%s: %s\n" % (k, r.headers[k])
    if len(r.history) > 0:
        s += "History: %s\n" % r.history
    s += "Content:\n%s\n" % r.content
    try:
        s += "JSON:\n%s\n" % r.json()
    except:
        pass
    return s


def retry_on_ConnectionError(exc):
    return isinstance(exc, requests.exceptions.ConnectionError)


@retry(stop_max_attempt_number=40, wait_fixed=250,
       retry_on_exception=retry_on_ConnectionError)
def acceptance_put(path, data):
    """
    keep trying a PUT until we don't get a ConnectionError,
    while we wait for it to come up.

    This waits up to 10 seconds, with 250ms between each try.
    Only retry on requests.exceptions.ConnectionError

    :param path: path to PUT to
    :type path: str
    :param data: data to PUT
    :type data: dict
    :return: response
    :rtype: requests.models.Response
    """
    if not path.startswith('/'):
        path = '/' + path
    url = 'http://localhost:8088%s' % path
    return requests.put(url, json=data)


class AcceptanceHelper(object):
    """
    Helper to run rpymostat (engine) inside `coverage`, for acceptance tests.
    """

    def __init__(self, args=['-vv']):
        """
        Initialize an AcceptanceHelper, with optional arguments to pass to
        `rpymostat`.

        :param args: optional arguments to pass to rpymostat
        :type args: list
        """
        self.args = ['coverage', 'run', '--branch', '--append', '-m',
                     'rpymostat.runner']
        self.args.extend(args)
        self.process = None
        self.stdout = None
        self.stderr = None
        self.returncode = None

    @property
    def out(self):
        return self.stdout

    @property
    def err(self):
        return self.stderr

    @property
    def return_code(self):
        return self.returncode

    def start(self):
        """
        Start the RPyMostat process.
        """
        travis_dir = os.environ.get('TRAVIS_BUILD_DIR', None)
        if travis_dir is not None:
            cwd = travis_dir
        else:
            cwd = os.path.abspath(
                os.path.join(os.path.abspath(__file__), '..', '..', '..')
            )
        self.process = Popen(self.args, cwd=cwd, stdout=PIPE, stderr=PIPE)

    def stop(self):
        """stop process with a CTRL_C_EVENT, simulating Ctrl+C / SIGINT"""
        # if we try to terminate() or kill(), coverage isn't recorded
        self.process.send_signal(SIGINT)
        stdout, stderr = self.process.communicate()
        if not isinstance(stdout, type('')):
            # python3 - they're bytes
            self.stdout = stdout.decode("utf-8")
            self.stderr = stderr.decode("utf-8")
        else:
            self.stdout = stdout
            self.stderr = stderr
        self.returncode = self.process.returncode

    def _error_for_assertion(self, expected, s):
        return 'expected "%s" to be in:\n%s' % (expected, s)

    def assert_in_out(self, s):
        """assert s in stdout; print a useful error message"""
        assert s in self.stdout, self._error_for_assertion(s, self.stdout)

    def assert_in_err(self, s):
        """assert s in stderr; print a useful error message"""
        assert s in self.stderr, self._error_for_assertion(s, self.stderr)
