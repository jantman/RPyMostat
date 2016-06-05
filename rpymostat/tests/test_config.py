"""
Tests for config.py

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

from rpymostat.config import Config

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, MagicMock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, MagicMock, DEFAULT  # noqa

pbm = 'rpymostat.config'
pb = '%s.Config' % pbm


class TestConfig(object):

    def setup(self):
        with patch('%s._get_from_env' % pb, autospec=True):
            self.cls = Config()
            self.cls._config_vars = {
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

    def test_init(self):
        with patch('%s._get_from_env' % pb, autospec=True) as mock_get_env:
            mock_get_env.return_value = {'foo': 'bar'}
            cls = Config()
        assert cls._config == {'foo': 'bar'}
        assert mock_get_env.mock_calls == [call(cls)]

    def test_get(self):
        self.cls._config = {'foo': 'bar', 'baz': 123}
        assert self.cls.get('foo') == 'bar'
        assert self.cls.get('baz') == 123

    def test_as_dict(self):
        d = {'foo': 'bar', 'baz': 123}
        self.cls._config = d
        assert self.cls.as_dict == d

    def test_get_from_env(self):
        with patch.dict(
            '%s.os.environ' % pbm,
            {
                'BAR': 'barEnv',
                'BLAM': '789'
            },
            clear=True
        ):
            res = self.cls._get_from_env()
        assert res == {
            'foo': 'fooDefault',
            'bar': 'barEnv',
            'baz': 123,
            'blam': 789
        }

    def test_get_var_info(self):
        assert self.cls.get_var_info() == self.cls._config_vars
