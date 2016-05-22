RPyMostat
=========

.. image:: https://pypip.in/v/rpymostat/badge.png
   :target: https://crate.io/packages/rpymostat

.. image:: https://pypip.in/d/rpymostat/badge.png
   :target: https://crate.io/packages/rpymostat


.. image:: https://secure.travis-ci.org/jantman/rpymostat.png?branch=master
   :target: http://travis-ci.org/jantman/rpymostat
   :alt: travis-ci for master branch

.. image:: https://codecov.io/github/jantman/rpymostat/coverage.svg?branch=master
   :target: https://codecov.io/github/jantman/rpymostat?branch=master
   :alt: coverage report for master branch

.. image:: http://www.repostatus.org/badges/0.1.0/concept.svg
   :alt: Project Status: Concept - Minimal or no implementation has been done yet.
   :target: http://www.repostatus.org/#concept

A python-based modular intelligent home thermostat, targeted at (but not requiring) the RaspberryPi and similar small computers, with a documented API. (Originally "RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too long to reasonably name a Python package).

Note that I attempted something like this `a long time ago <https://github.com/jantman/tuxostat>`_.

See docs/ for information.

This repository will hold the main Engine component

Architecture
------------

RPyMostat is made up of four components, each of which is distributed separately.
They can all be run on one host/RPi, or can be spread across multiple machines. All
components communicate over a documented HTTP ReST API, so aside from the Engine,
other components can be replaced with API-compatible versions written in other
languages or for specific hardware.

- Engine (this repo) - the "brains" which serve the API and make all decisions.
- UI - the Web UI, which is simply a web-based API client.
- Sensor - the temperature sensor daemon.
- Control - the physical relay control daemon.

Features
--------

Features planned for the initial release:

* Flexible rules-based scheduling. This can include cron-like schedules (do X at a given time of day, or time of day on one or more days of week, etc.), one-time schedule overrides ("I'm going to be away from December 21st to 28th this year, just keep the temperature above Y"), or instant adjustments ("make the temperature X degress NOW", in the web UI). The most specific schedule wins. Inital scheduling will support some mix of what can be represented by `ISO8601 time intervals <http://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`_ and `cron expressions <http://en.wikipedia.org/wiki/Cron#CRON_expression>`_.
* Data on current and desired temperature(s) and heating/cooling state will be collected. This should allow the scheduling engine to build up historical data on how long it takes to heat or cool one degree at a given temperature, and should allow us to trigger heating/cooling to reach the scheduled temperature at the scheduled time (as opposed to starting the heating/cooling at the scheduled time).
* Support for N temperature sensors, and scheduling based on them; i.e. set a daytime target temperature based on the temperature of your office, and a nighttime target based on the temperature in the bedroom.
* Web UI with robust mobile and touch support. Ideally, the entire system should be configurable by a web UI once it's installed (which should be done with a Puppet module).
* Some sort of physical on-the-wall touchscreen control, using the web UI.
* Everything AGPL 3.0.
* Ability to set schedules using a specific algorithm (plug-in architecture) and one or more specified temperature inputs.
* Scheduling and decision (system run) implemented in plugins (packages, `entry points <http://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`_) that use a defined API; some way of reflecting this in the Web UI (maybe this should come over the master API). Initially just implement scheduling as described above and setting temperature based on one temp input; subsequent plugins could include averaging across multiple inputs, weighted average, and predictive on/off cycles (including outside temperature input).
* Historical data stored in some time-series database; should include all temperature values at the beginning of a run, and every X minutes during a run.
* Everything should be modular.
* Support running all on one RPi, or splitting components apart; should support as many OSes as possible. Support for smaller devices as temperature sensors would be nice.
* Microservice/component architecture.
* Open, documented APIs. Aside from the main engine, it should be possible to implement the other components in other languages.
* mDNS / DNS-SD for zero configuration on devices other than the engine.

Reference Implementation
------------------------

My planned reference implementation of the system is:

* RaspberryPi physical control unit - USB relay output for control, and a temperature sensor, connecting via WiFi.

  * `DS18B20 <https://www.sparkfun.com/products/245>`_ temperature sensor using GPIO
  * For system control, either a `PiFace <https://www.sparkfun.com/products/11772>`_ or a `Phidgets 1014 <http://www.phidgets.com/products.php?product_id=1014>`_ USB 4 relay kit, both of which I already have.

* RaspberryPi temperature sensor in another room, connecting via WiFi.

  * `DS18B20 <https://www.sparkfun.com/products/245>`_ temperature sensor using GPIO

* Master control process, web UI and a third temperature input on my desktop computer.

  * `DS18S20 <https://www.sparkfun.com/products/retired/8366>`_ temperature sensor connected via `DS9490R <http://www.maximintegrated.com/en/products/comms/ibutton/DS9490R.html>`_ usb-to-1-wire adapter

Requirements
------------

* Python 2.7+ (currently tested with 2.7, 3.2, 3.3, 3.4)
* Python `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)

Installation
------------

It's recommended that you install into a virtual environment (virtualenv /
venv). See the `virtualenv usage documentation <http://www.virtualenv.org/en/latest/>`_
for information on how to create a venv. If you really want to install
system-wide, you can (using sudo).

.. code-block:: bash

    pip install rpymostat

Development
===========

To install for development:

1. Fork the `RPyMostat <https://github.com/jantman/RPyMostat>`_ repository on GitHub
2. Create a new branch off of master in your fork.

.. code-block:: bash

    $ virtualenv RPyMostat
    $ cd RPyMostat && source bin/activate
    $ pip install -e git+git@github.com:YOURNAME/rpymostat.git@BRANCHNAME#egg=rpymostat
    $ cd src/rpymostat

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

License
-------

RPyMostat is licensed under the `GNU Affero General Public License, version 3 or later <http://www.gnu.org/licenses/agpl.html>`_.

