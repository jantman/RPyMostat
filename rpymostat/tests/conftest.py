"""
RPyMostat conftest.py

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

import pytest
import sys
import os
import logging

# suppress docker logging
docker_log = logging.getLogger("docker")
docker_log.setLevel(logging.WARNING)
docker_log.propagate = True

# suppress requests logging
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True

HAVE_DOCKER = False
HAVE_MONGO = False

CONTAINER_NAME = 'rpymostat-pytest-mongodb24'
IMAGE_NAME = 'jantman/mongodb24'

try:
    from docker import Client
    HAVE_DOCKER = True
except ImportError:
    pass

try:
    from pymongo import MongoClient
    HAVE_MONGO = True
except ImportError:
    pass


def pytest_addoption(parser):
    """
    Add option to run Docker MongoDB container to pytest.
    """
    parser.addoption('--docker-mongo', action='store_true', default=False,
                     help='Run MongoDB Docker container if not TravisCI')


@pytest.fixture(scope="session", autouse=True)
def docker_mongodb(request):
    """
    Run jantman/mongodb24 container for DB tests.

    :param request: pytest config
    :type request: TestConfig::test_init
    :return: mongodb connection
    :rtype: pymongo.MongoClient
    """
    # don't do anything if we're not in an integration test environment
    if not request.config.getoption('--docker-mongo'):
        sys.stderr.write(
            "\nnot running mongodb - not specified on command line\n"
        )
        return None

    # raise if we can't import pymongo
    if not HAVE_MONGO:
        raise Exception("Could not import pymongo")

    # connect to the already-running MongoDB if we're in Travis
    if 'TRAVIS' in os.environ:
        sys.stderr.write(
            "\nnot running mongodb - running on TravisCI\n"
        )
        return mongo_connect(27017)

    # define a teardown function to clean up the container
    def docker_mongo_teardown():
        sys.stderr.write("\ntearing down mongodb docker container\n")
        teardown_docker_mongo()

    # raise if we can't import docker
    if not HAVE_DOCKER:
        raise Exception("Could not import docker")

    sys.stderr.write("\nstarting up mongodb docker container\n")
    try:
        mongo_port = setup_docker_mongo()
    except Exception as ex:
        teardown_docker_mongo()
        raise ex
    request.addfinalizer(docker_mongo_teardown)
    return mongo_connect(mongo_port)


def teardown_docker_mongo():
    if os.environ.get('LEAVE_MONGO_RUNNING', None) is not None:
        sys.stderr.write("Leaving MongoDB container running.\n")
        return
    c = Client(base_url='unix://var/run/docker.sock')
    destroy_container_if_exists(c)


def setup_docker_mongo():
    c = Client(base_url='unix://var/run/docker.sock')
    if os.environ.get('LEAVE_MONGO_RUNNING', None) is not None:
        cont_info = get_container_info(c, name=CONTAINER_NAME)
        if cont_info is not None:
            mongo_port = get_container_host_port(cont_info, 27017)
            sys.stderr.write("Using existing container %s on port %d\n" % (
                cont_info['Id'], mongo_port
            ))
            return mongo_port
    else:
        destroy_container_if_exists(c)
    # container is not already running
    pull_image(c)
    mongo_port = run_container(c)
    return mongo_port


def pull_image(c):
    """
    Pull the docker image.

    :param c: connected Docker client
    :type c: docker.client.Client
    """
    for img in c.images():
        for tag in img['RepoTags']:
            if tag == IMAGE_NAME or tag.startswith(IMAGE_NAME):
                sys.stderr.write('Using existing image %s (Id: %s)\n' % (
                                 tag, img['Id']))
                return
    sys.stderr.write('Pulling image: %s\n' % IMAGE_NAME)
    c.pull(IMAGE_NAME)


def get_container_info(c, name=None, cont_id=None):
    """
    Return dict of container information for the container with the given name

    :param c: connected Docker client
    :type c: docker.client.Client
    :returns: dict of information about container
    :rtype: dict
    """
    for cont in c.containers(all=True):
        if cont_id is not None and cont['Id'] == cont_id:
            return cont
        if name is not None and "/%s" % name in cont['Names']:
            return cont
    return None


def destroy_container_if_exists(c):
    """
    Destroy the container if it's already running.

    :param c: connected Docker client
    :type c: docker.client.Client
    """
    cont = get_container_info(c, name=CONTAINER_NAME)
    if cont is None:
        return
    sys.stderr.write(
        "Stopping and removing existing container %s\n" % cont['Id']
    )
    c.stop(cont['Id'])
    c.remove_container(cont['Id'])


def run_container(c):
    """
    Run the container for our tests.

    :param c: connected Docker client
    :type c: docker.client.Client
    :returns: MongoDB port
    :rtype: int
    """
    sys.stderr.write("Creating new container with name %s\n" % CONTAINER_NAME)
    cont = c.create_container(
        image=IMAGE_NAME,
        detach=True,
        ports=[27017, 27018],
        name=CONTAINER_NAME,
        host_config=c.create_host_config(
            port_bindings={
                27017: None,
                27018: None
            }
        )
    )
    sys.stderr.write("Container %s created; starting\n" % cont['Id'])
    c.start(cont['Id'])
    sys.stderr.write("Container %s started\n" % cont['Id'])
    cont_info = get_container_info(c, cont_id=cont['Id'])
    mongo_port = get_container_host_port(cont_info, 27017)
    return mongo_port


def get_container_host_port(cont, port_num):
    """
    Given a dict of information about a container, return the host port that
    ``port_num`` is bound to.

    :param cont: dict of container information
    :param port_num: container port number
    :return: int host port number
    """
    if 'Ports' not in cont:
        return None
    for p in cont['Ports']:
        if p['PrivatePort'] == port_num:
            return p['PublicPort']
    return None


def mongo_connect(port_num):
    """
    Return a connection to MongoDB. Keep trying until it's up.
    """
    c = MongoClient('localhost', port_num)
    count = 0
    while count < 20:
        try:
            sys.stderr.write(
                "Trying to connect to MongoDB on port %d\n" % port_num
            )
            assert 'local' in c.database_names()
            break
        except:
            pass
    else:
        raise Exception("Error: could not connect to MongoDB")
    sys.stderr.write("Connected to MongoDB\n")
    return c
