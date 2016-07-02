RPyMostat Development
=====================

To install for development:

1. Fork the `RPyMostat <https://github.com/jantman/RPyMostat>`_ repository on GitHub
2. Create a new branch off of master in your fork.

.. code-block:: bash

    $ git clone git@github.com:YOURNAME/RPyMostat.git
    $ cd RPyMostat
    $ virtualenv . && source bin/activate
    $ pip install -r requirements_dev.txt
    $ python setup.py develop

The git clone you're now in will probably be checked out to a specific commit,
so you may want to ``git checkout BRANCHNAME``.

Guidelines
----------

* pep8 compliant with some exceptions (see pytest.ini)
* 100% test coverage with pytest (with valid tests)

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`_, driven by `tox <http://tox.testrun.org/>`_.

* testing is as simple as:

  * ``pip install tox``
  * ``tox``

* If you want to see code coverage: ``tox -e cov``

  * this produces two coverage reports - a summary on STDOUT and a full report in the ``htmlcov/`` directory

* If you want to pass additional arguments to pytest, add them to the tox command line after "--". i.e., for verbose pytext output on py27 tests: ``tox -e py27 -- -v``

Acceptance Tests
----------------

Acceptance tests run against a real MongoDB. When running locally, they assume
that Docker is present and usable, and will pull and run a container from
`jantman/mongodb24 <https://hub.docker.com/r/jantman/mongodb24/>`_. When running
on TravisCI, they will use the `mongodb service <https://docs.travis-ci.com/user/database-setup/#MongoDB>`_
provided by Travis. The Travis MongoDB service currently `runs <https://travis-ci.org/jantman/RPyMostat>`_
2.4.12 as of 2016-06-11, which I'm considering close enough to the Debian 2.4.10
that we're targeting. If Travis upgrades that, we may need to look into alternate
ways of running Mongo for the Travis tests.

By default, when run locally, the acceptance tests will start up the MongoDB
container when the test session starts, and stop and remove it when the session
is over. To leave the container running and reuse it for further test sessions,
export the ``LEAVE_MONGO_RUNNING`` environment variable.

Release Checklist
-----------------

1. Open an issue for the release; cut a branch off master for that issue.
2. Confirm that there are CHANGES.rst entries for all major changes.
3. Ensure that Travis tests passing in all environments.
4. Ensure that test coverage is no less than the last release (ideally, 100%).
5. Increment the version number in RPyMostat/version.py and add version and release date to CHANGES.rst, then push to GitHub.
6. Confirm that README.rst renders correctly on GitHub.
7. Upload package to testpypi, confirm that README.rst renders correctly.

   * Make sure your ~/.pypirc file is correct
   * ``python setup.py register -r https://testpypi.python.org/pypi``
   * ``python setup.py sdist upload -r https://testpypi.python.org/pypi``
   * Check that the README renders at https://testpypi.python.org/pypi/rpymostat

8. Create a pull request for the release to be merge into master. Upon successful Travis build, merge it.
9. Tag the release in Git, push tag to GitHub:

   * tag the release. for now the message is quite simple: ``git tag -a vX.Y.Z -m 'X.Y.Z released YYYY-MM-DD'``
   * push the tag to GitHub: ``git push origin vX.Y.Z``

11. Upload package to live pypi:

    * ``python setup.py sdist upload``

10. make sure any GH issues fixed in the release were closed.
