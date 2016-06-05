"""
Main application entry point / runner for RPyMostat Engine.

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
import argparse
import logging

from twisted.web.server import Site
from twisted.internet import reactor
# @TODO: see http://twistedmatrix.com/documents/current/core/howto/logging.html
# and http://stackoverflow.com/questions/2493644/how-to-make-
# twisted-use-python-logging
from twisted.python.log import PythonLoggingObserver

from rpymostat.engine.apiserver import APIServer
from rpymostat.config import Config
from rpymostat.version import VERSION, PROJECT_URL

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] " \
         "%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()


def parse_args(argv):
    """
    Use Argparse to parse command-line arguments.

    :param argv: list of arguments to parse (``sys.argv[1:]``)
    :type argv: list
    :return: parsed arguments
    :rtype: :py:class:`argparse.Namespace`
    """
    p = argparse.ArgumentParser(
        description='RPyMostat Engine <%s>' % PROJECT_URL
    )
    p.add_argument('-c', '--show-config', dest='show_config',
                   action='store_true', default=False,
                   help='print configuration variable information')
    p.add_argument('-v', '--verbose', dest='verbose', action='count',
                   default=0,
                   help='verbose output. specify twice for debug-level '
                   'output.')
    p.add_argument('-V', '--version', action='version',
                   version='RPyMostat Engine v%s (<%s>)' % (
                       VERSION, PROJECT_URL
                   ))
    return p.parse_args(argv)


def show_config(conf):
    """
    Show configuration variable information.

    :param conf: config
    :type conf: :py:class:`~.Config`
    """
    sys.stderr.write("Configuration Environment Variables:\n")
    for varname, info in sorted(conf.get_var_info().items()):
        s = '%s (Default=%s' % (info['env_var_name'], info['default_value'])
        curr = conf.get(varname)
        if curr != info['default_value']:
            s += '; Current=%s' % curr
        if info['is_int']:
            s += '; int'
        s += ") %s\n" % info['description']
        sys.stderr.write(s)


def main(argv):
    """
    Run the Engine API server
    """
    # @TODO need setting for interface name to bind to (and address to
    # advertise); logic to find IP from ifname should go in -common, as
    # the control package will use it too. If not specified, default to
    # alphabetically-first non-loopback interface that has an address.
    conf = Config()
    args = parse_args(argv)
    if args.show_config:
        show_config(conf)
        raise SystemExit(1)
    logger.debug("instantiating apiserver")
    apiserver = APIServer()
    apisite = Site(apiserver.app.resource())
    logger.debug("reactor.listenTCP")
    reactor.listenTCP(conf.get('api_port'), apisite)
    logger.debug("reactor.run() - listening on port %d", conf.get('api_port'))
    # setup Python logging
    observer = PythonLoggingObserver()
    observer.start()
    reactor.run()
    logger.debug("run finished")


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
