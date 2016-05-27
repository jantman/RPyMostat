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
from twisted.web.server import Site
from twisted.internet import reactor
# @TODO: see http://twistedmatrix.com/documents/current/core/howto/logging.html
#  and http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging
from twisted.python import log

import logging

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()

from rpymostat import settings
from rpymostat.engine.apiserver import APIServer


def main():
    """
    Run the Engine API server
    """
    # @TODO need argument for interface name to bind to (and address to
    # advertise); logic to find IP from ifname should go in -common, as
    # the control package will use it too. If not specified, default to
    # alphabetically-first non-loopback interface that has an address.
    logger.debug("instantiating apiserver")
    apiserver = APIServer()
    apisite = Site(apiserver.app.resource())
    logger.debug("reactor.listenTCP")
    reactor.listenTCP(settings.API_PORT, apisite)
    logger.debug("reactor.run() - listening on port %d", settings.API_PORT)
    # setup Python logging
    observer = log.PythonLoggingObserver()
    observer.start()
    reactor.run()
    logger.debug("run finished")


if __name__ == "__main__":
    main()
