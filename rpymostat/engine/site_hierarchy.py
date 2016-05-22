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

import abc
import logging
from klein.app import Klein
from copy import deepcopy

logger = logging.getLogger(__name__)


class SiteHierarchy(object):
    """
    Helper class to implement hierarchical sites in Klein. All engine
    classes that provide routes must implement this.
    """
    __metaclass__ = abc.ABCMeta

    prefix_part = 'base'

    def __init__(self, app, parent_prefix):
        """
        Initialize a site hierarchy component. Takes the parent's prefix and
        sets up all routes under its own prefix. After classes implementing
        this interface are instantiated, their ``setup_routes`` method must
        be called.

        :param app: the Klein app to add routes in
        :type app: instance of :py:class:`klein.app.Klein`
        :param parent_prefix: The parent hierarchy's prefix
        :type parent_prefix: list of str
        """
        assert isinstance(app, Klein)
        assert isinstance(parent_prefix, type([]))
        assert self.prefix_part != 'base'
        self.prefix = self.make_prefix(parent_prefix, self.prefix_part)
        self.prefix_str = self.prefix_list_to_str(self.prefix)
        logger.debug('initializing prefix: %s', self.prefix_str)
        self.app = app

    def make_prefix(self, parent_list, prefix_str):
        """
        Given a list of the parent's prefix and our prefix string, construct
        a new list with our prefix.

        :param parent_list: parent's prefix
        :type parent_list: list
        :param prefix_str: our prefix string
        :type prefix_str: str
        :return: our prefix list
        :rtype: list
        """
        l = deepcopy(parent_list)
        l.append(prefix_str)
        return l

    def prefix_list_to_str(self, prefix_list):
        """
        Convert a prefix list to a string path prefix.

        :param prefix_list: the list to convert
        :type prefix_list: list
        :return: prefix string
        :rtype: str
        """
        return '/' + '/'.join(prefix_list)

    def add_route(self, func, path=None, methods=['GET']):
        """
        Add a route to app, mapping ``func`` (a callable method in this class)
        to ``path`` (under ``self.prefix``). If ``path`` is none, it will be
        mapped directly to ``self.prefix``.

        :param func: callable in this class to map to path
        :type func: method
        :param path: path to map method to
        :type path: str
        :param methods: methods allowed for this route
        :type methods: list
        """
        p = self.prefix_str
        if path is not None:
            p += '/' + path
        logger.debug('Adding route for %s to %s', p, func)
        self.app.route(p, methods=methods)(func)

    @abc.abstractmethod
    def setup_routes(self):
        """
        Setup all routes for this class. Must be implemented by subclasses.
        """
        raise NotImplementedError("setup_routes must be implemented in this "
                                  "class")
