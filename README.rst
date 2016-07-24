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

.. image:: https://badge.waffle.io/jantman/RPyMostat.png?label=ready&title=Ready
   :target: https://waffle.io/jantman/RPyMostat
   :alt: 'Stories in Ready - waffle.io'

.. image:: http://www.repostatus.org/badges/0.1.0/concept.svg
   :alt: Project Status: Concept - Minimal or no implementation has been done yet.
   :target: http://www.repostatus.org/#concept

A python-based modular intelligent home thermostat, targeted at (but not requiring) the RaspberryPi and similar small computers, with a documented open API. (Originally "RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too long to reasonably name a Python package).

Note that I attempted something like this `a long time ago <https://github.com/jantman/tuxostat>`_.

See docs/ for information.

This repository will hold the main Engine component

Status
------

Work-in-progress. Not even functional.

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

For further information, see the `architecture documentation <http://rpymostat.readthedocs.io/en/latest/Architecture.html>`_.

Features
--------

Features planned for the initial release:

* Flexible rules-based scheduling. This can include cron-like schedules (do X at a given time of day, or time of day on one or more days of week, etc.), one-time schedule overrides ("I'm going to be away from December 21st to 28th this year, just keep the temperature above Y"), or instant adjustments ("make the temperature X degress NOW", in the web UI). The most specific schedule wins. Inital scheduling will support some mix of what can be represented by `ISO8601 time intervals <http://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`_ and `cron expressions <http://en.wikipedia.org/wiki/Cron#CRON_expression>`_.
* Support for N temperature sensors, and scheduling based on them; i.e. set a daytime target temperature based on the temperature of your office, and a nighttime target based on the temperature in the bedroom.
* Web UI with robust mobile and touch support. Ideally, the entire system should be configurable by a web UI once it's installed (which should be done with a Puppet module).
* Some sort of physical on-the-wall touchscreen control, using the web UI.
* Everything AGPL 3.0.
* Scheduling and decision (system run) implemented in plugins (packages, `entry points <http://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`_) that use a defined API; some way of reflecting this in the Web UI (maybe this should come over the master API). Initially just implement scheduling as described above and setting temperature based on one temp input; subsequent plugins could include averaging across multiple inputs, weighted average, and predictive on/off cycles (including outside temperature input).
* Support running all on one RPi, or splitting components apart; should support as many OSes as possible. Support for smaller devices as temperature sensors would be nice.
* Microservice/component architecture.
* Open, documented APIs. Aside from the main engine, it should be possible to implement the other components in other languages.
* mDNS / DNS-SD for zero configuration on devices other than the engine.

Features planned for future releases:

* Data on current and desired temperature(s) and heating/cooling state will be collected. This should allow the scheduling engine to build up historical data on how long it takes to heat or cool one degree at a given temperature, and should allow us to trigger heating/cooling to reach the scheduled temperature at the scheduled time (as opposed to starting the heating/cooling at the scheduled time).
* Historical data stored in some time-series database; should include all temperature values at the beginning of a run, and every X minutes during a run.

Requirements
------------

* Python 2.7 or 3.3+ (currently tested with 2.7, 3.3, 3.4, 3.5; tested on pypy but does not support pypy3)
* Python `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)
* MongoDB (developed against 2.4, which is available in the Debian and Raspbian repos)

Installation, Configuration and Usage
-------------------------------------

See the `Installation, Configuration and Usage documentation <http://rpymostat.readthedocs.io/en/latest/Installation.html>`_.

Development
-----------

See the `development documentation <http://rpymostat.readthedocs.io/en/latest/development.html>`_.

License
-------

RPyMostat is licensed under the `GNU Affero General Public License, version 3 or later <http://www.gnu.org/licenses/agpl.html>`_.
