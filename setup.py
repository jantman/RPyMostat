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

from setuptools import setup, find_packages
from sys import version_info

from rpymostat.version import VERSION, PROJECT_URL

with open('README.rst') as file:
    long_description = file.read()

with open('CHANGES.rst') as file:
    long_description += '\n' + file.read()

requirements = [
    'Twisted>=14.0.0,<15.0.0',
    'klein',
    'txmongo',
    'pymongo>=3.0.0,<4.0.0'
]
    
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Environment :: No Input/Output (Daemon)',
    'Framework :: Twisted',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Topic :: Home Automation',
]

extras = {
    'hub': ['foo'],
}

setup(
    name='rpymostat',
    version=VERSION,
    author='Jason Antman',
    author_email='jason@jasonantman.com',
    packages=find_packages(),
    url=PROJECT_URL,
    license='AGPLv3+',
    entry_points="""
    [console_scripts]
    rpymostat-engine = rpymostat.runner:main
    """,
    description='A python-based modular intelligent home thermostat, targeted at (but not requiring) the RaspberryPi and similar small computers, with a documented open API.',
    long_description=long_description,
    install_requires=requirements,
    extra_requires=extras,
    keywords="temperature thermometer nest thermostat automation control home",
    classifiers=classifiers
)
