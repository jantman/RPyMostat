Planning
========

|Project Status: Concept - Minimal or no implementation has been done
yet.|

A python-based intelligent home thermostat, targeted at (but not
requiring) the RaspberryPi and similar small computers. (Originally
"RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too
long to reasonably name a Python package).

Especially since the introduction of the `Nest
thermostat <http://en.wikipedia.org/w/index.php?title=Nest_Labs&redirect=no>`__,
a lot of people have attempted a project like this. I'd like to think
that mine is different - perhaps more polished, perhaps it stores
historical data in a real, logical way. Multiple temperatures are nice,
and the pluggable scheduling and decision engines are something I
haven't seen in any others yet. The completely open API, and the fact
that some of the out-of-the-box components use it is new too. And after
looking at some of the options out there, I think the idea of it being
packaged and distributed properly is pretty novel too, as are my hopes
for a platform-agnostic system; a lot of the options out there are
really hardware-hacking projects, and I want to make software that works
with as many hardware options as it can. But when it comes down to it,
this is an idea that I tried `a long time
ago <https://github.com/jantman/tuxostat>`__ and never finished, and
want to have another try at regardless of whether it does something
unique or becomes just another one of the hundred pieces of software
that do the same thing. I'm also going to be playing with some
technology that I've never used before, so for me this is as much about
learning and exploring as it is about producing a polished final
codebase.

See:

-  `Architecture.md <Architecture.md>`__ for an overview of the
   architecture, and most of the documentation that currently exists.
-  `DISCOVERY.md <DISCOVERY.md>`__ for some information on service
   discovery
-  `TWISTED.md <TWISTED.md>`__ for some docs on using Twisted for this

Features
--------

Features planned for the initial release
++++++++++++++++++++++++++++++++++++++++

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

Features planned for future releases
++++++++++++++++++++++++++++++++++++

* Data on current and desired temperature(s) and heating/cooling state will be collected. This should allow the scheduling engine to build up historical data on how long it takes to heat or cool one degree at a given temperature, and should allow us to trigger heating/cooling to reach the scheduled temperature at the scheduled time (as opposed to starting the heating/cooling at the scheduled time).
* Historical data stored in some time-series database; should include all temperature values at the beginning of a run, and every X minutes during a run.

Relevant Links / Similar Projects
---------------------------------

-  https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
-  https://www.adafruit.com/product/1012
-  http://www.projects.privateeyepi.com/home/temperature-gauge
-  http://m.instructables.com/id/Raspberry-Pi-Temperature-Humidity-Network-Monitor/
-  `Raspberry Pi Thermostat Part 1: System Overview - The
   Nooganeer <http://www.nooganeer.com/his/projects/homeautomation/raspberry-pi-thermostat-part-1-overview/>`__
-  `Willseph/RaspberryPiThermostat <https://github.com/Willseph/RaspberryPiThermostat>`__
-  `python - Thermostat Control Algorithms - Stack
   Overflow <http://stackoverflow.com/questions/8651063/thermostat-control-algorithms>`__
-  `VE2ZAZ - Smart Thermostat on the Raspberry
   Pi <http://ve2zaz.net/RasTherm/RasTherm.htm>`__
-  `Raspberry Pi • View topic - Web enabled thermostat
   project <http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=24115>`__
-  `Rubustat - the Raspberry Pi Thermostat \| Wyatt Winters \| Saving
   the world one computer at a
   time <http://wyattwinters.com/rubustat-the-raspberry-pi-thermostat.html>`__
-  `Makeatronics: Raspberry Pi Thermostat
   Hookups <http://makeatronics.blogspot.com/2013/04/raspberry-pi-thermostat-hookups.html>`__
-  `Makeatronics: Thermostat
   Software <http://makeatronics.blogspot.com/2013/04/thermostat-software.html>`__
-  `Willseph/RaspberryPiThermostat: A Raspberry Pi-powered smart
   thermostat written in Python and
   PHP. <https://github.com/Willseph/RaspberryPiThermostat>`__ - Python
   sensors and control but PHP LAMP web UI. MIT license. Looks like it's
   got a good bit of information, especially on wiring/setup and photos
   of the install on `Imgur <http://imgur.com/gallery/YxElS>`__.
-  `ianmtaylor1/thermostat: Raspberry Pi Thermostat
   code <https://github.com/ianmtaylor1/thermostat>`__ - Python project
   that reads 1-wire temps and uses SQLAlchemy. Relatively simple beyond
   that.
-  `chaeron/thermostat: Raspberry Pi
   Thermostat <https://github.com/chaeron/thermostat>`__ - Fairly nice
   touchscreen UI and pretty complete, but one untested python file and
   only one physical piece.
-  `mharizanov/ESP8266\_Relay\_Board: Three Channel WiFi
   Relay/Thermostat
   Board <https://github.com/mharizanov/ESP8266_Relay_Board>`__ -
   firmware source code and hardware designs for a WiFi relay/thermostat
   board. Probably won't use this, but interesting.
-  `mdarty/thermostat: Raspberry Pi Thermostat
   Controller <https://github.com/mdarty/thermostat>`__ - python/flask
   app for a Python RPi thermostat.
-  `tom91136/thermostat: A simple thermostat for RaspberryPi written in
   Python <https://github.com/tom91136/thermostat>`__ - Another Flask,
   DS18B20 thermostat with GPIO relays.
-  `jeffmcfadden/PiThermostat: Build a Raspberry Pi
   Thermostat <https://github.com/jeffmcfadden/PiThermostat>`__ - Rails
   app for an RPi thermostat.
-  `Forever-Young/thermostat-web: Django application for thermostat
   control <https://github.com/Forever-Young/thermostat-web>`__ -
   single-host
-  `wywin/Rubustat: A thermostat controller for Raspberry Pi on
   Flask <https://github.com/wywin/Rubustat>`__
-  `tommybobbins/PiThermostat: Raspberry Pi, TMP102 and 433 Transmitter
   to make an Redis based Central heating
   system <https://github.com/tommybobbins/PiThermostat>`__ -
   Redis-based system using Google Calendar for scheduling
-  `jpardobl/django-thermostat: Django app to control a
   heater <https://github.com/jpardobl/django-thermostat>`__
-  `tinkerjs/Pi-Thermostat: A Raspberry Pi based
   thermostat <https://github.com/tinkerjs/Pi-Thermostat>`__ - Python
   and RPi, but single-host. `Blog
   post <http://technicalexplorer.blogspot.com/2015/08/the-thermostat.html>`__
   has some nice diagrams, pictures, and information on HVAC systems.
-  `cakofony/thermostat: Web enabled thermostat project to run on the
   raspberry pi. <https://github.com/cakofony/thermostat>`__ - Python,
   includes support for an Adafruit character LCD display.
-  `Raspberry Pi Thermostat Part 1: System Overview - The
   Nooganeer <http://www.nooganeer.com/his/projects/homeautomation/raspberry-pi-thermostat-part-1-overview/>`__
   - nice web UI demo
-  `VE2ZAZ - Smart Thermostat on the Raspberry
   Pi <http://ve2zaz.net/RasTherm/RasTherm.htm>`__ - Flask UI
-  `openHAB <http://www.openhab.org/>`__ - JVM-based, vendor-agnostic
   home automation "hub". Includes web UI. Rule creation appears to be
   via a Java UI though.
-  `home-assistant/home-assistant: Open-source home automation platform
   running on Python
   3 <https://github.com/home-assistant/home-assistant>`__ - Python3
   home automation server with web UI. Looks like it could be really
   interesting, but not sure how much support it has for the advanced
   scheduling I want.
-  `WTherm – a smart thermostat \|
   NiekProductions <http://niekproductions.com/p/wtherm/>`__ - Arduino,
   PHP but has some good concepts.
-  `Home \| pimatic - smart home automation for the raspberry
   pi <https://pimatic.org/>`__ - node.js home automation framework.
   Once again, doesn't have support for the kind of scheduling I want.
-  `Matt Brenner / PyStat ·
   GitLab <https://gitlab.com/madbrenner/PyStat>`__ - multi-threaded
   Ptrhon thermostat; Flask, RPi.
   `screenshots <http://imgur.com/a/7vkZO>`__. Looks nice, but doesn't
   seem to have the type of scheduling I want, and runs as a single
   process/single host.
-  `serial\_device2 <https://pypi.python.org/pypi/serial_device2/1.0>`__
   - Extends serial.Serial to add methods such as auto discovery of
   available serial ports in Linux, Windows, and Mac OS X
-  `pyusbg2 <https://pypi.python.org/pypi/pyusbg2>`__ - PyUSB offers
   easy USB devices communication in Python. It should work without
   additional code in any environment with Python >= 2.4, ctypes and an
   pre-built usb backend library (currently, libusb 0.1.x, libusb 1.x,
   and OpenUSB).

Some Technical Bits and Questions
---------------------------------

API
+++

-  `raml <http://raml.org/>`__ - RESTful API Modeling Language
-  `architecting version-less
   APIs <http://urthen.github.io/2013/05/16/ways-to-version-your-api-part-2/>`__

Engine
++++++

-  The main process will likely have to have a number of threads: API
   serving (ReST API), timer/cron for scheduling and comparing temp
   values to thresholds, main thread (am I missing anything?)
- Use workers (either real Celery, or just async calling a process/thread) to
  calculate things?
- schedules and overrides
- schedules have start and end time, that are cron-like
- overrides have a specific start time, and end time that's either specific (input can be a specific datetime, or a duration) or when the next schedule starts
- backend - when a schedule or override is input, backend recalculates the next X hours of instructions (schedule with overrides applied), caches them, makes them accessible via API
- schedules and overrides
- default temperature thresholds (how much over/under to trigger/overshoot and how often to run)
- schedules/overrides have temperature targets and thresholds - which sensors to look at, how to weight them. Can be a "simple" input (look at only one sensor, one target temp) or a weighted combination. Can save a default calculation method/sensor weighting.
- make sure we don't start/stop the system too often

UI
+++

-  Web UI will probably use Flask, **TODO:** but I need to figure out
   how easy it is to get that to just wrap an API.
-  **TODO:** Is there any way that we can generate (dynamically? code generation?) the API server and client? The web UI? Is there an existing web UI "thing" to just wrap a ReST API? Would this help testing?
-  I know some of the python API clients I've worked with do this... I just need to figure out how, because it's an area I've never really looked into.
- Just provide a pretty (or usable) wrapper around the decision engine API. Honestly I'd love it if this could be generated entirely dynamically - i.e. the decision engine's plugins know about some input data types, and the web UI knows how to render them. The web UI is just a pile of components, and pulls information about what it needs dynamically from the decision engine. That's really complicated to implement, but OTOH, I'm not sure how else we allow pluggable scheduling and decision modules.
- visual schedule overlay like PagerDuty

Testing
+++++++

-  Assuming we're going with the API-based model, unit tests should be
   simple. Integration and acceptance tests are another question.
-  **TODO:** How to test the API server and client?
-  **TODO:** How to test the separate services, in isolation from the
   server?
-  just a concern for testing the API client. this should be simple
   enough.
-  **TODO:** Try to find a strong unit testing framework for the web UI;
   we can deal with integration/acceptance testing later.
-  `pytest-flask <https://pypi.python.org/pypi/pytest-flask>`__ looks
   like it should handle things quite well
-  **TODO:** How do I do acceptance/integration testing with service
   discovery if I have this running (like, in my house) on my LAN? Just
   use some "system number" variable?



Relay/Physical Control Unit
+++++++++++++++++++++++++++

dead-simple:

1. Process starts up, uses service discovery to find the decision
   engine.
2. Registers itself with some sort of unique ID (hardware UUID,
   RaspberryPi serial number, etc.)
3. Discovers available relay outputs and their states, assigns a unique
   ID to each.
4. POST this information to the decision engine.
5. Start a web server.
6. Wait for an API request from the decision engine, which is either a
   GET (current status) or POST (set state).

Decision Engine / Master Control Process
++++++++++++++++++++++++++++++++++++++++

Here's where the complexity lies.

-  Keep (time-series?) database of historical data on temperature,
   system state, etc. (including data required for predictive system
   operation)
-  Determine the current and next (N) schedules.
-  Constantly (every N seconds) compare temperature data to current
   schedule and operate system accordingly
-  Re-read schedules whenever a change takes place
-  Show end-user current system state and upcoming schedules
-  Provide a plugin interface for schedule algorithms
-  Provide a plugin interface for decision (system run/stop) algorithms
-  Support third-party web UIs via its API, which needs to include
   support for the plug-in scheduling and decision algorithms (which
   exist only in this process, not the web UI)
-  Support versioning of ReST and internal APIs

Datastore
+++++++++

When I'd initially planned this project (circa 2014) I'd planned on using a NoSQL document store, and was leaning towards MongoDB - mainly because I don't know where the project will go, and I want to support plugins, so a schemaless DB is an advantage (and migrations are a pain). However, as of mid-2016, MongoDB has dropped support for 32-bit architectures and modern versions simply don't run on the RaspberryPi anymore. Saying that users need a separate machine to run the DB goes against the philosophy of this project (though it's how I'll be running my installation), and also introduces reliability and power stability issues. I *really* wanted Mongo, but it doesn't look like that is happening.

Unless I can find another NoSQL document store that runs well on the Pi, I'm going to go with a standard RDBMS; most likely SQLite for test/evaluation and PostgreSQL (or MySQL) for production use. I don't want the overhead of an ORM for something that should be this simple, so I'll use raw SQL, but that means (as far as I can tell) handling migrations myself

Migrations
~~~~~~~~~~

- When the Engine starts it makes an initial DB connection. It attempts to read a ``version`` from the ``db_version`` table.
- If the table doesn't exist, we run an SQL file (included in the package) or a series of SQL statements, to setup the latest DB schema version.
- If the table does exist, we grab the ``db_version`` (int) and run all migrations from that version to the current one (once again, either SQL files in the package or a Python script with SQL statements to run).
- This means that I'll need to manually maintain the migrations for every version. This sounds awful, but with proper discipline, it's really not: all I need is to not make any changes directly to the DB, but rather make them in the migration files. When I start work on a new version, I create a migration file for the next DB version. In development, I have a helper command that can create a dev database initialized to any DB version, or can run migrations on the current DB, to test the code I've written. When I release a new version, if there are any migrations, I also create a schema dump of the current DB.

Twisted DB Info
~~~~~~~~~~~~~~~

- `FrequentlyAskedQuestions – Twisted <https://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#HowcanIaccessself.factoryfrommyProtocols__init__>`_
- `[Twisted-Python] Sharing a database connection in web server <https://twistedmatrix.com/pipermail/twisted-python/2013-December/027863.html>`_
- `Example – Using Non-Global State — Klein 15.3.1 documentation <http://klein.readthedocs.io/en/latest/examples/nonglobalstate.html>`_
- `alex/alchimia <https://github.com/alex/alchimia>`_ allows use of `SQLAlchemy <http://www.sqlalchemy.org/>`_ core (not ORM) from Twisted
   (`SQLAlchemy features <http://www.sqlalchemy.org/features.html>`_). `alembic <https://pypi.python.org/pypi/alembic>`_ is a SQLAlchemy
   migration tool, so is `sqlalchemy-migrate <https://sqlalchemy-migrate.readthedocs.io/en/latest/>`_.
- `random project from GitHub <https://github.com/TechEmpower/FrameworkBenchmarks/blob/dd906d0d9ee51c633c40704606de377f11c821a4/frameworks/Python/klein/app.py>`_ that
   uses SQLAlchemy ORM with Klein.

Physical Control Interface
++++++++++++++++++++++++++

-  Wall mount tablet for the UI? There's some
   `cheap <http://www.amazon.com/s/ref=sr_st_price-asc-rank?lo=computers&rh=n%3A172282%2Cn%3A!493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077590011&qid=1463663130&sort=price-asc-rank>`__
   ones, and `AutoStart - No root - Android Apps on Google
   Play <https://play.google.com/store/apps/details?id=com.autostart&hl=en>`__
   to autostart an app (browser) at boot...
- Wall mount touchscreens:
  - https://www.adafruit.com/products/1892
  - https://www.adafruit.com/products/2033
  - https://www.adafruit.com/products/2534
  - https://www.adafruit.com/products/2260
  - Could just use an old phone for now... or set it up somewhere on a bookcase or table...
  - https://blog.adafruit.com/2014/09/05/wall-mounted-touchscreen-raspberry-pi-home-server-piday-raspberrypi-raspberry_pi/
  - http://www.neosecsolutions.com//products.php?62&cPath=21
  - http://www.modmypi.com/blog/raspberry-pi-7-touch-sreen-display-case-assembly-instructions
  - http://www.thingiverse.com/thing:1082431
  - http://www.thingiverse.com/thing:1034194
  - https://www.element14.com/community/docs/DOC-78156/l/raspberry-pi-7-touchscreen-display
- Pi3 Model B - $35-40 - - https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
  - wifi (2.4GHz 802.11n??? - might need USB?)
  - USB
  - GPIO
  - HDMI
  - DSI display interface
- Pi Zero - https://www.raspberrypi.org/products/pi-zero/ - sold out everywhere :(
  - Mini HDMI
  - USB On-The-Go
  - MicroUSB power
  - HAT-compatible 40-pin header
  - onboard wifi hack: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=127449
  - starter kit - https://www.adafruit.com/products/2816
  - would need USB WiFi dongle and GPIO sensors
- RPi DS18B20
  - https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
  - https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
  - http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
  - https://www.raspberrypi.org/forums/viewtopic.php?t=54238&p=431812

Other Hardware
--------------

-  `Miniature WiFi 802.11b/g/n Module: For Raspberry Pi and more ID: 814
   - $11.95 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/814>`__
-  `USB WiFi 802.11b/g/n Module: For Raspberry Pi and more ID: 1012 -
   $12.95 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/product/1012>`__
-  `Assembled Pi Cobbler Plus - Breakout Cable for Pi B+/A+/Pi 2/Pi 3
   ID: 2029 - $6.95 : Adafruit Industries, Unique & fun DIY electronics
   and kits <https://www.adafruit.com/products/2029>`__
-  `Assembled Pi T-Cobbler Plus - GPIO Breakout for RasPi A+/B+/Pi 2/Pi
   3 ID: 2028 - $7.95 : Adafruit Industries, Unique & fun DIY
   electronics and kits <https://www.adafruit.com/products/2028>`__
-  `GPIO Header for Raspberry Pi A+/B+/Pi 2/Pi 3 2x20 Female Header ID:
   2222 - $1.50 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/2222>`__
-  `0.1 2x20-pin Strip Right Angle Female Header ID: 2823 - $1.50 :
   Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/2823>`__
