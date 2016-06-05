"""
Tests for runner.py

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

from rpymostat import runner

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, MagicMock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, MagicMock, DEFAULT  # noqa

pbm = 'rpymostat.runner'


class TestRunnerMocked(object):
    """
    Tests the runner functions with mocked objects; no actual Twisted testing
    """

    def test_main(self):
        """
        test main function
        """
        with patch('%s.logger' % pbm, autospec=True) as mocklogger:
            with patch.multiple(
                pbm,
                autospec=True,
                APIServer=DEFAULT,
                Site=DEFAULT,
                reactor=DEFAULT,
                PythonLoggingObserver=DEFAULT,
            ) as mocks:
                runner.main()
        assert mocks['APIServer'].mock_calls == [
            call(),
            call().app.resource()
        ]
        site_app_res = mocks[
            'APIServer'].return_value.app.resource.return_value
        assert mocks['Site'].mock_calls == [
            call(site_app_res)
        ]
        assert mocks['reactor'].mock_calls == [
            call.listenTCP(8088, mocks['Site'].return_value),
            call.run()
        ]
        assert mocks['PythonLoggingObserver'].mock_calls == [
            call(),
            call().start()
        ]
        assert mocklogger.mock_calls == [
            call.debug('instantiating apiserver'),
            call.debug("reactor.listenTCP"),
            call.debug("reactor.run() - listening on port %d", 8088),
            call.debug("run finished")
        ]
