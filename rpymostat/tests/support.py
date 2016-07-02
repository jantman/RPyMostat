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
import time


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

    def start(self):
        """
        Start the RPyMostat process.
        """
        cwd = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))
        self.process = Popen(self.args, cwd=cwd, stdout=PIPE, stderr=PIPE)

    def stop(self):
        self.process.terminate()
        count = 0
        while count < 100:
            if self.process.pid is not None:
                self.process.kill()
                time.sleep(0.1)
            else:
                break
        self.stdout, self.stderr = self.process.communicate()
        self.returncode = self.process.returncode
