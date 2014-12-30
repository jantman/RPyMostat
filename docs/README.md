RPyMostat
=========

[![Project Status: Concept - Minimal or no implementation has been done yet.](http://www.repostatus.org/badges/0.1.0/concept.svg)](http://www.repostatus.org/#concept)

A python-based intelligent home thermostat, targeted at (but not requiring) the RaspberryPi and similar small computers. (Originally "RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too long to reasonably name a Python package).

Note that I attempted something like this [a long time ago](https://github.com/jantman/tuxostat).

See:

* [Architecture.md](Architecture.md) for an overview of the architecture, and most of the documentation that currently exists.
* [DISCOVERY.md](DISCOVERY.md) for some information on service discovery
* [TWISTED.md](TWISTED.md) for some docs on using Twisted for this

ToDo
----

* sphinx docs (and gh-pages for the site)
* figure out packaging
* decide on nomenclature for the various parts, and update docs to reflect it

Features
--------

Features planned for the initial release:

* Flexible rules-based scheduling. This can include cron-like schedules (do X at a given time of day, or time of day on one or more days of week, etc.), one-time schedule overrides ("I'm going to be away from December 21st to 28th this year, just keep the temperature above Y"), or instant adjustments ("make the temperature X degress NOW", in the web UI). The most specific schedule wins. Inital scheduling will support some mix of what can be represented by [ISO8601 time intervals](http://en.wikipedia.org/wiki/ISO_8601#Time_intervals) and [cron expressions](http://en.wikipedia.org/wiki/Cron#CRON_expression).
* Data on current and desired temperature(s) and heating/cooling state will be collected. This should allow the scheduling engine to build up historical data on how long it takes to heat or cool one degree at a given temperature, and should allow us to trigger heating/cooling to reach the scheduled temperature at the scheduled time (as opposed to starting the heating/cooling at the scheduled time).
* Support for N temperature sensors, and scheduling based on them; i.e. set a daytime target temperature based on the temperature of your office, and a nighttime target based on the temperature in the bedroom.
* Web UI with robust mobile support. Ideally, the entire system should be configurable by a web UI once it's installed (which should be done with a Puppet module).
* I don't plan on supporting physical controls (screen and buttons on the wall) any time soon; in practice, I'm always closer to a laptop, tablet or phone than I am to that one out-of-the-way spot on the wall.
* Everything AGPL 3.0.
* Ability to set schedules using a specific algorithm (plug-in architecture) and one or more specified temperature inputs.
* Scheduling and decision (system run) implemented in plugins (packages, [entry points](http://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins)) that use a defined API; some way of reflecting this in the Web UI (maybe this should come over the master API). Initially just implement scheduling as described above and setting temperature based on one temp input; subsequent plugins could include averaging across multiple inputs, weighted average, and predictive on/off cycles (including outside temperature input).
* Historical data stored in some time-series database; should include all temperature values at the beginning of a run, and every X minutes during a run.
* Everything should be modular.
* Support running all on one RPi, or splitting components apart; should support as many OSes as possible. Support for smaller devices as temperature sensors would be nice.

Reference Implementation
------------------------

My planned reference implementation of the system is:

* RaspberryPi physical control unit - USB relay output for control, and a temperature sensor, connecting via WiFi.
    * [DS18B20](https://www.sparkfun.com/products/245) temperature sensor using GPIO
    * For system control, either a [PiFace](https://www.sparkfun.com/products/11772) or a [Phidgets 1014](http://www.phidgets.com/products.php?product_id=1014) USB 4 relay kit, both of which I already have.
* RaspberryPi temperature sensor in another room, connecting via WiFi.
    * [DS18B20](https://www.sparkfun.com/products/245) temperature sensor using GPIO
* Master control process, web UI and a third temperature input on my desktop computer.
    * [DS18S20](https://www.sparkfun.com/products/retired/8366) temperature sensor connected via [DS9490R](http://www.maximintegrated.com/en/products/comms/ibutton/DS9490R.html) usb-to-1-wire adapter

Relevant Links
---------------

* https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
* https://www.adafruit.com/product/1012
* http://www.projects.privateeyepi.com/home/temperature-gauge
* http://m.instructables.com/id/Raspberry-Pi-Temperature-Humidity-Network-Monitor/
* [serial_device2](https://pypi.python.org/pypi/serial_device2/1.0) - Extends serial.Serial to add methods such as auto discovery of available serial ports in Linux, Windows, and Mac OS X
* [pyusbg2](https://pypi.python.org/pypi/pyusbg2) - PyUSB offers easy USB devices communication in Python. It should work without additional code in any environment with Python >= 2.4, ctypes and an pre-built usb backend library (currently, libusb 0.1.x, libusb 1.x, and OpenUSB).

Some Technical Bits and Questions
----------------------------------

* Sphinx and ReadTheDocs for docs (should start on this sooner rather than later).
* TravisCI and pytest for testing. Might need to look into the special cases if we do a lot of threading, or use Twisted.
* Web UI will probably use Flask, __TODO:__ but I need to figure out how easy it is to get that to just wrap an API.
* Assuming we're going with the API-based model, unit tests should be simple. Integration and acceptance tests are another question.
* __TODO:__ How to test the API server and client?
* __TODO:__ How to test the separate services, in isolation from the server?
  * just a concern for testing the API client. this should be simple enough.
* __TODO:__ Try to find a strong unit testing framework for the web UI; we can deal with integration/acceptance testing later.
  * [pytest-flask](https://pypi.python.org/pypi/pytest-flask) looks like it should handle things quite well
* __TODO:__ Is there any way that we can generate (dynamically? code generation?) the API server and client? The web UI? Is there an existing web UI "thing" to just wrap a ReST API? Would this help testing?
  * I know some of the python API clients I've worked with do this... I just need to figure out how, because it's an area I've never really looked into.
  * Not sure how to handle this programmatically, as most ReST API tools are built to be part of a web application, which this isn't.
  * [Flask API](https://github.com/tomchristie/flask-api) looks OK but development seems to have stopped and there are many issues
  * [Restless](https://github.com/toastdriven/restless) a generic ReST "miniframework", intended for Python web frameworks
  * A quick [Flask ReST API tutorial](http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) [and another](http://blog.luisrei.com/articles/flaskrest.html)
  * [eve](http://python-eve.org/) a "ReST API framework in a box" using Flask, MongoDB and Redis.
  * [Flask-restful](https://github.com/flask-restful/flask-restful) and its [quickstart](http://flask-restful.readthedocs.org/en/latest/quickstart.html)
  * [raml](http://raml.org/) - RESTful API Modeling Language
  * [architecting version-less APIs](http://urthen.github.io/2013/05/16/ways-to-version-your-api-part-2/)
  * [web development with Twisted](http://twistedmatrix.com/trac/wiki/WebDevelopmentWithTwisted)
  * [web services with twisted](http://zenmachine.wordpress.com/web-services-and-twisted/)
  * [Building RESTful, Service-Oriented Architectures with Twisted](http://lanyrd.com/2012/pycon-za/syyfm/) video and slide deck
  * [Twisted community code and add-ons](https://twistedmatrix.com/trac/wiki/ProjectsUsingTwisted)
* Maybe a lot of this should use message queues instead of HTTP APIs. But we'd need a message broker, and AFAIK few of them are lightweight (though Celery supports Redis, RabbitMQ, or using MongoDB or SQLAlchemy).
* __TODO:__ How do I do acceptance/integration testing with service discovery if I have this running (like, in my house) on my LAN? Just use some "system number" variable?
* The main process will likely have to have a number of threads: API serving (ReST API), timer/cron for scheduling and comparing temp values to thresholds, main thread (am I missing anything?)
  * Should we use [Twisted](https://twistedmatrix.com/trac/)?
  * If so, can we use pytest for it (unit tests)? looks like yes - [pytest-twisted](https://github.com/schmir/pytest-twisted), [pytest docs](http://pytest.org/latest/faq.html#how-does-pytest-relate-to-twisted-s-trial), [twisted's testing docs](https://twistedmatrix.com/documents/14.0.0/core/howto/trial.html) which focus on their unittest-like [trial](http://twistedmatrix.com/trac/wiki/TwistedTrial) framework ([also this](http://twistedmatrix.com/documents/14.0.0/core/development/policy/test-standard.html)), a [random blog post](http://www.mechanicalcat.net/richard/log/Python/Tips_for_Testing_Twisted) on testing Twisted without Trial.
  * Should we just do threading ourselves? If so, is there anything to help with the API?
  * How do we do integration tests?
  * Flask [might](http://stackoverflow.com/a/22900255/211734) be able to do this, but [this](http://stackoverflow.com/a/24101692/211734) implies otherwise. It supports celery [but as a separate process](http://flask.pocoo.org/docs/0.10/patterns/celery/).
  * Twisted [Klein](http://klein.readthedocs.org/en/latest/) might be the union of what I need; here's [a tutorial](http://tavendo.com/blog/post/going-asynchronous-from-flask-to-twisted-klein/).
* Temperature and control daemons can probably be single-threaded, the logic there is pretty simple. Timeouts should do all we need.
  * [bottle](http://bottlepy.org/docs/dev/index.html) might be a simple option
* Web UI can just be a normal webapp, all it does is provide a graphical interface to the decision engine API
* __TODO:__ what database to use?
  * Mongo? [MongoEngine](http://mongoengine.org/) (mongo "orm")
* Scheduling
  * implement it from scratch?
* Crazy thought: maybe adding an API onto the decision engine process is a bad idea. Maybe I should think a little less "tiny system" - maybe some sort of message queue is the right idea, or we should have a "main process" that simply stores data and provides a ReST API (and maybe the Web UI too?) and have a scheduling engine that's a separate thing?

What the Processes Need to Do
-----------------------------

### Web UI

Just provide a pretty (or usable) wrapper around the decision engine API. Honestly I'd love it if this could be generated entirely dynamically - i.e. the decision engine's plugins know about some input data types, and the web UI knows how to render them. The web UI is just a pile of components, and pulls information about what it needs dynamically from the decision engine. That's really complicated to implement, but OTOH, I'm not sure how else we allow pluggable scheduling and decision modules.

### Temperature Sensors

Dead-simple:

1. Process starts up, uses service discovery to find the decision engine.
2. Registers itself with some sort of unique ID (hardware UUID, RaspberryPi serial number, etc.)
3. Discovers available temperature sensors, and some sort of unique (never-changing) ID for each.
4. Reads values from sensors, POST to decision engine API.
5. Repeat #4 indefinitely. (if connection to decision engine goes away, start back at #1).

### Relay/Physical Control Unit

Also dead-simple:

1. Process starts up, uses service discovery to find the decision engine.
2. Registers itself with some sort of unique ID (hardware UUID, RaspberryPi serial number, etc.)
3. Discovers available relay outputs and their states, assigns a unique ID to each.
4. POST this information to the decision engine.
5. Start a web server.
6. Wait for an API request from the decision engine, which is either a GET (current status) or POST (set state).

### Decision Engine / Master Control Process

Here's where the complexity lies.

* Run a web server for the ReST API used by the other services (including the Web UI).
* Maintain database of all configuration and settings; versioning and ORM?
* Ability to store configuration to push to other daemons (like temperature polling rate).
* Keep (time-series?) database of historical data on temperature, system state, etc. (including data required for predictive system operation)
* Determine the current and next (N) schedules.
* Constantly (every N seconds) compare temperature data to current schedule and operate system accordingly
* Re-read schedules whenever a change takes place
* Show end-user current system state and upcoming schedules
* Provide a plugin interface for schedule algorithms
* Provide a plugin interface for decision (system run/stop) algorithms
* Support third-party web UIs via its API, which needs to include support for the plug-in scheduling and decision algorithms (which exist only in this process, not the web UI)
* Support versioning of ReST and internal APIs

From a threading or work-oriented model, this boils down to:

1. Main thread
2. ReST API
3. Database(s)?
4. Schedule determination and temperature evaluation (these could be triggered events based on a timer or some action/signal)

Twisted supports scheduling/timeouts/repeating events, which seems like it could handle quite a bit of this.

Framework Considerations
=========================

There are essentially two options (aside from doing it all from scratch) that appear obvious:

1. An async/event processing framework (Twisted) with ReST bolted on
2. A web framework with async/event processing bolted on

The main concerns/evaluation points that I can think of:

* ReST API serving (data to/from the database, and shared/main thread memory)
* Signals or some other sort of notification mechanism
* Scheduled tasks
* Database access from multiple threads (whatever we use as a datastore, and whatever we use as a TSDB)
* test-ability (i.e. pytest, possibly something else to test the threading/network)

Datastore
==========

NoSQL or document-object sounds good, since for the most part we're storing simple objects, but
they may have arbitrary properties (plugins). And schema migrations are a pain. But I'm not sure
how these work on tiny systems; Mongo is the most popular, but it's certainly not geared towards
one node with a small amount of memory and CPU (and disk).

TSDB
=====

We want to store historical data on temperatures, runs, etc. Initially we can just use something simple, but
we'll probably want to find a good, optimized storage for this.

Packaging
==========

[qwcode](https://github.com/qwcode) suggested using one repository and setuptools extras. I did some tests to make sure `pip` supports them correctly.

Using the default `pip` on my machine, I had some issues. However, if I upgraded to the latest `pip` (6.0.3 at this time), most common requirement patterns worked fine:

* `projectname[extra]`
* `projectname[extra]>=X.Y.Z`
* `projectname[extra] <massive version spec here, like: ">0.0.3,<0.0.6,!=0.0.4">`
* `[-e] (git+git|git+https)://url#egg=projectname[extra]`
* `[-e] (git+git|git+https)://url@<hash or branch or tag>#egg=projectname[extra]`
* `-e /path/to/local/git/clone/of/projectname[extra]`

The only supported specifiers that don't seem to handle installing the extras are:

* `/path/to/local/git/clone/of/projectname[extra]` (note, without `-e`)
* `file:///path/to/archive/of/project.zip[extra]`

__Question:__ will this work with multiple extras? (i.e. `[hub,sensor,control]`)

So, with this, my plan is going to be:

* `rpymostat` - central, shared code and the decision engine ("hub"?)
  * install as `rpymostat[hub]` (or via requirements files) for the hub dependencies
* `rpymostat-webui` - separate repo, separate distribution
* `rpymostat-sensor` - separate repo, separate distribution
* `rpymostat-relays` - separate repo, separate distribution

I haven't yet decided if I'm going to use [namespace packages](http://pythonhosted.org/setuptools/setuptools.html#namespace-packages). That would
be more logical and elegant (i.e. `rpymostat.sensor` instead of `rpymostat_sensor`). My only reservation is if I'm claiming to have a pluggable
architecture (i.e. the sensor, relay or web UI can be replaced with a third party one that just respects our API), maybe these things should be
relatively separate in order to promote that?
