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
from klein import Klein
from rpymostat.engine.site_hierarchy import SiteHierarchy

import pytest

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'rpymostat.engine.site_hierarchy'
pb = '%s.SiteHierarchy' % pbm


class TestClass(SiteHierarchy):

    prefix_part = 'v1'

    def setup_routes(self):
        pass


class BadBaseTestClass(SiteHierarchy):

    def setup_routes(self):
        pass


class TestSiteHierarchy(object):

    def setup(self):
        self.app = Mock(spec=Klein)
        self.prefix = ['my', 'parent']
        self.cls = TestClass(self.app, self.prefix)

    def test_class(self):
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch.multiple(
                pb,
                autospec=True,
                make_prefix=DEFAULT,
                prefix_list_to_str=DEFAULT,
            ) as mocks:
                mocks['make_prefix'].return_value = ['foo', 'bar']
                mocks['prefix_list_to_str'].return_value = 'foo/bar'
                cls = TestClass(self.app, self.prefix)
        assert mocks['make_prefix'].mock_calls == [
            call(cls, self.prefix, 'v1')
        ]
        assert mocks['prefix_list_to_str'].mock_calls == [
            call(cls, ['foo', 'bar'])
        ]
        assert mock_logger.mock_calls == [
            call.debug('initializing prefix: %s', 'foo/bar')
        ]
        assert cls.prefix == ['foo', 'bar']
        assert cls.prefix_str == 'foo/bar'
        assert cls.app == self.app

    def test_class_not_klein(self):
        with pytest.raises(AssertionError):
            TestClass(Mock(), self.prefix)

    def test_class_prefix_not_list(self):
        with pytest.raises(AssertionError):
            TestClass(self.app, 'foo')

    def test_class_prefix_part_base(self):
        with pytest.raises(AssertionError):
            BadBaseTestClass(self.app, self.prefix)

    def test_make_prefix(self):
        assert self.cls.make_prefix(
            ['foo', 'bar'], 'baz') == ['foo', 'bar', 'baz']

    def test_prefix_list_to_str(self):
        assert self.cls.prefix_list_to_str([]) == '/'
        assert self.cls.prefix_list_to_str(
            ['foo']) == '/foo'
        assert self.cls.prefix_list_to_str(
            ['foo', 'bar', 'baz']) == '/foo/bar/baz'

    def test_add_route_default_methods_no_path(self):
        mock_func = Mock()
        self.cls.prefix_str = '/my/prefix'
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            self.cls.add_route(mock_func)
        assert self.app.mock_calls == [
            call.route('/my/prefix', methods=['GET']),
            call.route()(mock_func)
        ]
        assert mock_logger.mock_calls == [
            call.debug('Adding route for %s to %s', '/my/prefix', mock_func)
        ]

    def test_add_route_POST_with_path(self):
        mock_func = Mock()
        self.cls.prefix_str = '/my/prefix'
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            self.cls.add_route(mock_func, path='foo', methods=['POST'])
        assert self.app.mock_calls == [
            call.route('/my/prefix/foo', methods=['POST']),
            call.route()(mock_func)
        ]
        assert mock_logger.mock_calls == [
            call.debug('Adding route for %s to %s', '/my/prefix/foo', mock_func)
        ]
