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

from rpymostat.runner import main, parse_args, show_config
from rpymostat.version import PROJECT_URL, VERSION
from rpymostat.config import Config

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'rpymostat.runner'


class TestRunnerMocked(object):
    """
    Tests the runner functions with mocked objects; no actual Twisted testing
    """

    def test_main(self):
        """
        test main function
        """

        def se_config_get(name):
            if name == 'api_port':
                return 8088
            return None

        mock_args = Mock(verbose=0, show_config=False)
        with patch('%s.logger' % pbm, autospec=True) as mocklogger:
            with patch.multiple(
                pbm,
                autospec=True,
                APIServer=DEFAULT,
                Site=DEFAULT,
                reactor=DEFAULT,
                PythonLoggingObserver=DEFAULT,
                parse_args=DEFAULT,
                show_config=DEFAULT,
                Config=DEFAULT,
            ) as mocks:
                mocks['Config'].return_value.get.side_effect = se_config_get
                mocks['parse_args'].return_value = mock_args
                main([])
        assert mocks['show_config'].mock_calls == []
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

    def test_parse_args(self):
        with patch('%s.argparse.ArgumentParser' % pbm, autospec=True) as mock_p:
            parse_args([])
        assert mock_p.mock_calls == [
            call(description='RPyMostat Engine <%s>' % PROJECT_URL),
            call().add_argument('-c', '--show-config', dest='show_config',
                                action='store_true', default=False,
                                help='print configuration variable information'
                                ),
            call().add_argument('-v', '--verbose', dest='verbose',
                                action='count', default=0,
                                help='verbose output. specify twice for '
                                     'debug-level output.'),
            call().add_argument('-V', '--version', action='version',
                                version='RPyMostat Engine v%s (<%s>)' % (
                                    VERSION, PROJECT_URL)),
            call().parse_args([])
        ]

    def test_parse_args_default(self):
        res = parse_args([])
        assert res.verbose == 0
        assert res.show_config is False

    def test_parse_args_verbose1(self):
        res = parse_args(['-v'])
        assert res.verbose == 1

    def test_parse_args_verbose2(self):
        res = parse_args(['-vv'])
        assert res.verbose == 2

    def test_parse_args_show_config(self):
        res = parse_args(['--show-config'])
        assert res.show_config is True

    def test_show_config(self, capsys):
        with patch('rpymostat.config.Config._get_from_env',
                   autospec=True) as mock_config_get_env:
            mock_config_get_env.return_value = {
                'foo': 'fooDefault',
                'bar': 'barEnv',
                'baz': 123,
                'blam': 789
            }
            conf = Config()
        conf._config_vars = {
            'foo': {
                'env_var_name': 'FOO',
                'description': 'fooDesc',
                'is_int': False,
                'default_value': 'fooDefault'
            },
            'bar': {
                'env_var_name': 'BAR',
                'description': 'barDesc',
                'is_int': False,
                'default_value': 'barDefault'
            },
            'baz': {
                'env_var_name': 'BAZ',
                'description': 'bazDesc',
                'is_int': True,
                'default_value': 123
            },
            'blam': {
                'env_var_name': 'BLAM',
                'description': 'blamDesc',
                'is_int': True,
                'default_value': 456
            }
        }
        show_config(conf)
        exp_err = "Configuration Environment Variables:\n"
        exp_err += "BAR (Default=barDefault; Current=barEnv) barDesc\n"
        exp_err += "BAZ (Default=123; int) bazDesc\n"
        exp_err += "BLAM (Default=456; Current=789; int) blamDesc\n"
        exp_err += "FOO (Default=fooDefault) fooDesc\n"
        out, err = capsys.readouterr()
        assert out == ''
        assert err == exp_err
