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

A python-based intelligent home thermostat, targeted at (but not requiring) the RaspberryPi and similar small computers. (Originally "RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too long to reasonably name a Python package).

Note that I attempted something like this `a long time ago<https://github.com/jantman/tuxostat>`_.

See:

* `docs/Architecture.md<docs/Architecture.md>`_ for an overview of the architecture, and most of the documentation that currently exists.
* `docs/DISCOVERY.md<docs/DISCOVERY.md>`_ for some information on service discovery
* `docs/PACKAGING.md<docs/PACKAGING.md>`_ for elaboration on how to package and distribute all this

Features
--------

Features planned for the initial release:

* Flexible rules-based scheduling. This can include cron-like schedules (do X at a given time of day, or time of day on one or more days of week, etc.), one-time schedule overrides ("I'm going to be away from December 21st to 28th this year, just keep the temperature above Y"), or instant adjustments ("make the temperature X degress NOW", in the web UI). The most specific schedule wins. Inital scheduling will support some mix of what can be represented by `ISO8601 time intervals<http://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`_ and `cron expressions<http://en.wikipedia.org/wiki/Cron#CRON_expression>`_.
* Data on current and desired temperature(s) and heating/cooling state will be collected. This should allow the scheduling engine to build up historical data on how long it takes to heat or cool one degree at a given temperature, and should allow us to trigger heating/cooling to reach the scheduled temperature at the scheduled time (as opposed to starting the heating/cooling at the scheduled time).
* Support for N temperature sensors, and scheduling based on them; i.e. set a daytime target temperature based on the temperature of your office, and a nighttime target based on the temperature in the bedroom.
* Web UI with robust mobile support. Ideally, the entire system should be configurable by a web UI once it's installed (which should be done with a Puppet module).
* I don't plan on supporting physical controls (screen and buttons on the wall) any time soon; in practice, I'm always closer to a laptop, tablet or phone than I am to that one out-of-the-way spot on the wall.
* Everything AGPL 3.0.
* Ability to set schedules using a specific algorithm (plug-in architecture) and one or more specified temperature inputs.
* Scheduling and decision (system run) implemented in plugins (packages, `entry points<http://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`_) that use a defined API; some way of reflecting this in the Web UI (maybe this should come over the master API). Initially just implement scheduling as described above and setting temperature based on one temp input; subsequent plugins could include averaging across multiple inputs, weighted average, and predictive on/off cycles (including outside temperature input).
* Historical data stored in some time-series database; should include all temperature values at the beginning of a run, and every X minutes during a run.
* Everything should be modular.
* Support running all on one RPi, or splitting components apart; should support as many OSes as possible. Support for smaller devices as temperature sensors would be nice.

Reference Implementation
------------------------

My planned reference implementation of the system is:

* RaspberryPi physical control unit - USB relay output for control, and a temperature sensor, connecting via WiFi.

    * `DS18B20<https://www.sparkfun.com/products/245>`_ temperature sensor using GPIO
    * For system control, either a `PiFace<https://www.sparkfun.com/products/11772>`_ or a `Phidgets 1014<http://www.phidgets.com/products.php?product_id=1014>`_ USB 4 relay kit, both of which I already have.

* RaspberryPi temperature sensor in another room, connecting via WiFi.

    * `DS18B20<https://www.sparkfun.com/products/245>`_ temperature sensor using GPIO

* Master control process, web UI and a third temperature input on my desktop computer.

    * `DS18S20<https://www.sparkfun.com/products/retired/8366>`_ temperature sensor connected via `DS9490R<http://www.maximintegrated.com/en/products/comms/ibutton/DS9490R.html>`_ usb-to-1-wire adapter
