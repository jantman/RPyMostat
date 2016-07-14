Planning
========

A python-based intelligent home thermostat, targeted at (but not
requiring) the RaspberryPi and similar small computers. (Originally
"RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too
long to reasonably name a Python package).

Especially since the introduction of the `Nest
thermostat <http://en.wikipedia.org/w/index.php?title=Nest_Labs&redirect=no>`_,
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
ago <https://github.com/jantman/tuxostat>`_ and never finished, and
want to have another try at regardless of whether it does something
unique or becomes just another one of the hundred pieces of software
that do the same thing. I'm also going to be playing with some
technology that I've never used before, so for me this is as much about
learning and exploring as it is about producing a polished final
codebase.

See:

-  `Architecture.md <Architecture.md>`_ for an overview of the
   architecture, and most of the documentation that currently exists.
-  `DISCOVERY.md <DISCOVERY.md>`_ for some information on service
   discovery
-  `TWISTED.md <TWISTED.md>`_ for some docs on using Twisted for this

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
   Nooganeer <http://www.nooganeer.com/his/projects/homeautomation/raspberry-pi-thermostat-part-1-overview/>`_
-  `Willseph/RaspberryPiThermostat <https://github.com/Willseph/RaspberryPiThermostat>`_
-  `python - Thermostat Control Algorithms - Stack
   Overflow <http://stackoverflow.com/questions/8651063/thermostat-control-algorithms>`_
-  `VE2ZAZ - Smart Thermostat on the Raspberry
   Pi <http://ve2zaz.net/RasTherm/RasTherm.htm>`_
-  `Raspberry Pi • View topic - Web enabled thermostat
   project <http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=24115>`_
-  `Rubustat - the Raspberry Pi Thermostat \| Wyatt Winters \| Saving
   the world one computer at a
   time <http://wyattwinters.com/rubustat-the-raspberry-pi-thermostat.html>`_
-  `Makeatronics: Raspberry Pi Thermostat
   Hookups <http://makeatronics.blogspot.com/2013/04/raspberry-pi-thermostat-hookups.html>`_
-  `Makeatronics: Thermostat
   Software <http://makeatronics.blogspot.com/2013/04/thermostat-software.html>`_
-  `Willseph/RaspberryPiThermostat: A Raspberry Pi-powered smart
   thermostat written in Python and
   PHP. <https://github.com/Willseph/RaspberryPiThermostat>`_ - Python
   sensors and control but PHP LAMP web UI. MIT license. Looks like it's
   got a good bit of information, especially on wiring/setup and photos
   of the install on `Imgur <http://imgur.com/gallery/YxElS>`_.
-  `ianmtaylor1/thermostat: Raspberry Pi Thermostat
   code <https://github.com/ianmtaylor1/thermostat>`_ - Python project
   that reads 1-wire temps and uses SQLAlchemy. Relatively simple beyond
   that.
-  `chaeron/thermostat: Raspberry Pi
   Thermostat <https://github.com/chaeron/thermostat>`_ - Fairly nice
   touchscreen UI and pretty complete, but one untested python file and
   only one physical piece.
-  `mharizanov/ESP8266\_Relay\_Board: Three Channel WiFi
   Relay/Thermostat
   Board <https://github.com/mharizanov/ESP8266_Relay_Board>`_ -
   firmware source code and hardware designs for a WiFi relay/thermostat
   board. Probably won't use this, but interesting.
-  `mdarty/thermostat: Raspberry Pi Thermostat
   Controller <https://github.com/mdarty/thermostat>`_ - python/flask
   app for a Python RPi thermostat.
-  `tom91136/thermostat: A simple thermostat for RaspberryPi written in
   Python <https://github.com/tom91136/thermostat>`_ - Another Flask,
   DS18B20 thermostat with GPIO relays.
-  `jeffmcfadden/PiThermostat: Build a Raspberry Pi
   Thermostat <https://github.com/jeffmcfadden/PiThermostat>`_ - Rails
   app for an RPi thermostat.
-  `Forever-Young/thermostat-web: Django application for thermostat
   control <https://github.com/Forever-Young/thermostat-web>`_ -
   single-host
-  `wywin/Rubustat: A thermostat controller for Raspberry Pi on
   Flask <https://github.com/wywin/Rubustat>`_
-  `tommybobbins/PiThermostat: Raspberry Pi, TMP102 and 433 Transmitter
   to make an Redis based Central heating
   system <https://github.com/tommybobbins/PiThermostat>`_ -
   Redis-based system using Google Calendar for scheduling
-  `jpardobl/django-thermostat: Django app to control a
   heater <https://github.com/jpardobl/django-thermostat>`_
-  `tinkerjs/Pi-Thermostat: A Raspberry Pi based
   thermostat <https://github.com/tinkerjs/Pi-Thermostat>`_ - Python
   and RPi, but single-host. `Blog
   post <http://technicalexplorer.blogspot.com/2015/08/the-thermostat.html>`_
   has some nice diagrams, pictures, and information on HVAC systems.
-  `cakofony/thermostat: Web enabled thermostat project to run on the
   raspberry pi. <https://github.com/cakofony/thermostat>`_ - Python,
   includes support for an Adafruit character LCD display.
-  `Raspberry Pi Thermostat Part 1: System Overview - The
   Nooganeer <http://www.nooganeer.com/his/projects/homeautomation/raspberry-pi-thermostat-part-1-overview/>`_
   - nice web UI demo
-  `VE2ZAZ - Smart Thermostat on the Raspberry
   Pi <http://ve2zaz.net/RasTherm/RasTherm.htm>`_ - Flask UI
-  `openHAB <http://www.openhab.org/>`_ - JVM-based, vendor-agnostic
   home automation "hub". Includes web UI. Rule creation appears to be
   via a Java UI though.
-  `home-assistant/home-assistant: Open-source home automation platform
   running on Python
   3 <https://github.com/home-assistant/home-assistant>`_ - Python3
   home automation server with web UI. Looks like it could be really
   interesting, but not sure how much support it has for the advanced
   scheduling I want.
-  `WTherm – a smart thermostat \|
   NiekProductions <http://niekproductions.com/p/wtherm/>`_ - Arduino,
   PHP but has some good concepts.
-  `Home \| pimatic - smart home automation for the raspberry
   pi <https://pimatic.org/>`_ - node.js home automation framework.
   Once again, doesn't have support for the kind of scheduling I want.
-  `Matt Brenner / PyStat ·
   GitLab <https://gitlab.com/madbrenner/PyStat>`_ - multi-threaded
   Ptrhon thermostat; Flask, RPi.
   `screenshots <http://imgur.com/a/7vkZO>`_. Looks nice, but doesn't
   seem to have the type of scheduling I want, and runs as a single
   process/single host.
-  `serial\_device2 <https://pypi.python.org/pypi/serial_device2/1.0>`_
   - Extends serial.Serial to add methods such as auto discovery of
   available serial ports in Linux, Windows, and Mac OS X
-  `pyusbg2 <https://pypi.python.org/pypi/pyusbg2>`_ - PyUSB offers
   easy USB devices communication in Python. It should work without
   additional code in any environment with Python >= 2.4, ctypes and an
   pre-built usb backend library (currently, libusb 0.1.x, libusb 1.x,
   and OpenUSB).

Some Technical Bits and Questions
---------------------------------

API
+++

-  `raml <http://raml.org/>`_ - RESTful API Modeling Language
-  `architecting version-less
   APIs <http://urthen.github.io/2013/05/16/ways-to-version-your-api-part-2/>`_

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
- [tastejs/todomvc: Helping you select an MV* framework - Todo apps for Backbone.js, Ember.js, AngularJS, and many more](https://github.com/tastejs/todomvc) / [TodoMVC](http://todomvc.com/)
- https://en.wikipedia.org/wiki/HATEOAS
- **looks good** - [Writing a Javascript REST client - miguelgrinberg.com](http://blog.miguelgrinberg.com/post/writing-a-javascript-rest-client) - [Twitter Bootstrap](http://twitter.github.io/bootstrap/) for presentation (see [fluid layout model](http://getbootstrap.com/2.3.2/examples/fluid.html)), [Knockout](http://knockoutjs.com/) for MVC.
- [vinta/awesome-python: A curated list of awesome Python frameworks, libraries, software and resources](https://github.com/vinta/awesome-python#database-drivers)
- [Ajenti Core - a Web-UI Toolkit](http://ajenti.org/core/) - has a really nice UI, and is Python on the backend
- [Backbone.js](http://backbonejs.org/) - might be good... it's an in-browser MVC. A little worried about memory use.
- [Creating a Single Page Todo App with Node and Angular | Scotch](https://scotch.io/tutorials/creating-a-single-page-todo-app-with-node-and-angular)

Testing
+++++++

- Unit tests should mock out the txmongo connection. Integration tests require
  Mongo, and should run a Docker container of it. Need to look into how to do
  this nicely on Travis.
- We'll need some real data fixtures, and to look into the right way to dump
  and load data from/to Mongo.
-  Assuming we're going with the API-based model, unit tests should be
   simple. Integration and acceptance tests are another question.
-  **TODO:** How to test the API server and client?
-  **TODO:** How to test the separate services, in isolation from the
   server?
-  **TODO:** Try to find a strong unit testing framework for the web UI;
   we can deal with integration/acceptance testing later.
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

MongoDB 2.4. Raspbian has it for ARM.

- `txmongo <https://github.com/twisted/txmongo>`_ and its `docs <https://txmongo.readthedocs.io/en/latest/>`_
- txmongo `twisted.web example <https://github.com/twisted/txmongo/blob/master/examples/webapps/twistedweb_server.tac>`_

Time-Series:

- `Schema Design for Time Series Data in MongoD - MongoDB Blog <http://blog.mongodb.org/post/65517193370/schema-design-for-time-series-data-in-mongodb>`_
- `Time Series <http://learnmongodbthehardway.com/schema/chapter6/>`_
- `MongoDB for Time Series Data Part 1: Setting the Stage for Sensor Management | MongoDB <https://www.mongodb.com/presentations/mongodb-time-series-data-part-1-setting-stage-sensor-management>`_
- `MongoDB for Time Series Data | MongoDB <https://www.mongodb.com/presentations/mongodb-time-series-data>`_
- `Efficient storage of non-periodic time series with MongoDB <https://bluxte.net/musings/2015/01/21/efficient-storage-non-periodic-time-series-mongodb/>`_
- `Capped Collections — MongoDB Manual 3.2 <https://docs.mongodb.com/manual/core/capped-collections/>`_
- `MongoDB tech behind our time series graphs - 30TB per month <https://blog.serverdensity.com/tech-behind-time-series-graphs-2bn-docs-per-day-30tb-per-month/>`_
- `Make Interactive Time Series Charts for IoT Using Live MongoDB Data | SlamData <http://slamdata.com/news-and-blog/2016/04/18/make-interactive-time-series-charts-for-iot-using-live-mongodb-data/>`_
- `Storing time-series data with MongoDB and TokuMX <https://www.percona.com/blog/2015/05/26/storing-time-series-data-with-mongodb-and-tokumx/>`_
- `MongoDB Time Series: Introducing the Aggregation Framework - DZone Database <https://dzone.com/articles/mongodb-time-series>`_
- `comSysto Blog: Processing and analysing sensor data <https://comsysto.com/blog-post/processing-and-analysing-sensor-data>`_
- `MongoDB time series: Introducing the aggregation framework | Vlad Mihalcea's Blog <https://vladmihalcea.com/2014/01/10/mongodb-time-series-introducing-the-aggregation-framework/>`_

Physical Control Interface
++++++++++++++++++++++++++

-  Wall mount tablet for the UI? There's some
   `cheap <http://www.amazon.com/s/ref=sr_st_price-asc-rank?lo=computers&rh=n%3A172282%2Cn%3A!493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077590011&qid=1463663130&sort=price-asc-rank>`_
   ones, and `AutoStart - No root - Android Apps on Google
   Play <https://play.google.com/store/apps/details?id=com.autostart&hl=en>`_
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
   kits <https://www.adafruit.com/products/814>`_
-  `USB WiFi 802.11b/g/n Module: For Raspberry Pi and more ID: 1012 -
   $12.95 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/product/1012>`_
-  `Assembled Pi Cobbler Plus - Breakout Cable for Pi B+/A+/Pi 2/Pi 3
   ID: 2029 - $6.95 : Adafruit Industries, Unique & fun DIY electronics
   and kits <https://www.adafruit.com/products/2029>`_
-  `Assembled Pi T-Cobbler Plus - GPIO Breakout for RasPi A+/B+/Pi 2/Pi
   3 ID: 2028 - $7.95 : Adafruit Industries, Unique & fun DIY
   electronics and kits <https://www.adafruit.com/products/2028>`_
-  `GPIO Header for Raspberry Pi A+/B+/Pi 2/Pi 3 2x20 Female Header ID:
   2222 - $1.50 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/2222>`_
-  `0.1 2x20-pin Strip Right Angle Female Header ID: 2823 - $1.50 :
   Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/2823>`_
