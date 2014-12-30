from setuptools import setup
from sys import version_info

from rpymostat.version import VERSION

with open('README.rst') as file:
    long_description = file.read()

with open('CHANGES.rst') as file:
    long_description += '\n' + file.read()

requirements = [
    'Twisted>=14.0.0,<15.0.0',
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
    packages=find_packages()
    url='http://github.com/jantman/RPyMostat/',
    license='AGPLv3+',
    description='A python-based intelligent home thermostat, targeted at (but not requiring) the RaspberryPi and similar small computers.',
    long_description=long_description,
    install_requires=requirements,
    extra_requires=extras,
    keywords="thermostat automation control temperature",
    classifiers=classifiers
)
