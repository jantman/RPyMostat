This reproduces a Gist that I published [here](https://gist.github.com/jantman/d38ae4552c5a78cee6af) and asked for feedback on. My current working theory is listed at the bottom.

Python Packaging Conundrum
===========================

I'm starting work on a new [project](https://github.com/jantman/RPyMostat/tree/PoC) and can't decide how to package and distribute it properly.

The project a set of distributed processes that communicate over a ReST API, essentially a client-server model (well, to simplify things). The general layout of code and what will be running is:

* Some shared objects and modules (including an API client for the main decision engine)
* a main decision engine that handles database communication, business logic, etc. (runs as its own daemon)
* a standalone web UI that communicates with the main decision engine over its API (runs as its own daemon)
* two different small standalone daemons which gather data and forward it to the main process over its API

The standalone daemons are targeted at lightweight hardware (the [RaspberryPi](http://www.raspberrypi.org/) initially, but should be able to run on something like the [Arduino](http://arduino.cc/) or even smaller). As such, these should be able to be installed and run without pulling in all of the requirements of the main engine (database bindings, etc.).

Some other miscellaneous notes:

* Code will live on GitHub
* docs will be done via Sphinx to [readthedocs.org](https://readthedocs.org/)
* TravisCI for testing
* will be installed via `pip` in a virtualenv, so should be using setuptools (and should be installable in develop/editable mode)

The Questions
--------------

So... how do I lay out the source and package/distribute all this?

I can think of a few immediately obvious possibilities:

1. _Five_ (5) totally separate repositories, maintained and installed as separate things (separate distributions). This means five separate sources of documentation (though they could be cross-referenced via inter-sphinx mapping). It also means a maintenance headache as the decision engine and the core/shared libraries (including the API client for the decision engine) would need to be kept in sync.
1. A single repository, split into (python) packages, but installed and managed as one distribution. Docs would be in one place. AFAIK pip/setuptools doesn't have any way to install "sub-distributions", so pip (`setup.py` `install_requires`) would only install the minimum common set of requirements, and the user would have to `pip install -r` the appropriate requirements file for the pieces they want to run.
1. Some sort of hackery/magic using setuptools [namespace packages](http://pythonhosted.org/setuptools/setuptools.html#namespace-packages) and [extras](http://pythonhosted.org/setuptools/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies). Namespace packages would let us package the shared/core libraries and main decision logic in one distribution (the web UI and standalone daemons would still be separate packages, but that might be good, as it makes it simpler and clearer for third-parties to replace or extend them). Extras sound like we *might* be able to use them (the feature is explicitly designed to handle optional requirements) _but_ I don't see any clear way to handle them with pip. Perhaps the way to go about this (really sounds like a hack) is to put all of the code for the core/shared stuff and the decision engine in one repository/distribution, setup the extra requirements, and then have a decision engine "dummy" package that just serves to install the extra requirements?
1. ???

Is there a more elegant way to do this? If I were doing this with OS packages (i.e. RPMs), I could use a single source tree to generate multiple installable packages (distributions) each with different requirements, but the Python packaging world doesn't seem to have anything analagous (and `pip` wouldn't support installing it from a GIT url, so that's a dealbreaker).

Any suggestions from someone who knows more about this than I do?

Working Theory
==============

Just go with #1 above, use five separate distributions/repositories:

* The Web UI, temperature sensor daemons and physical control daemons will be managed as separate Git repositories, which become separate Python distributions (i.e. `rpymostat_sensor`, `rpymostat_control`, etc.).
  * Different package names internally. At this point I'm leaning towards _not_ using [namespace packages](http://pythonhosted.org/setuptools/setuptools.html#namespace-packages)
  * Helps enforce thinking of these as dogfooding our plugin API, and that they can be swapped out trivially (they're separate projects that just consume the API, and share only certain well-defined bits of code).
  * Docs will be built separately, but can link using [intersphinx mapping](http://sphinx-doc.org/ext/intersphinx.html)
  * These will all require a common, top-level `rpymostat` distribution which provides common shared code.
* `rpymostat` distribution (and package) provides shared top-level code (including decision engine API client) and minimum dependencies
  * this means we need to manage the client and server as two separate projects, but once again, this is logical if we want to claim an open architecture.
* `rpymostat_engine` distribution is the "master control process"
  * includes numerous external dependencies for things like database, etc.
  * makes extensive use of code in the main `rpymostat` distribution
  * I considered the idea of building both the API client and server off of some common code in the shared package, but that might violate some of our "anyone can implement an API client" concepts

So, assuming this is what we go with, we'd have five Git repositories, each with their own distribution and their own docs:

* `rpymostat` - central, shared code (like our service discovery wrappers)
* `rpymostat-engine` - decision engine, its API, DB services, etc.
* `rpymostat-webui` - the Web UI application
* `rpymostat-sensor` - temperature sensor daemon
* `rpymostat-relays` - the physical relay control daemon

The one remaining question is how we handle namespaces. It would be logical to use [namespace packages](http://pythonhosted.org/setuptools/setuptools.html#namespace-packages)
and put this all under a `rpymostat` namespace (and this would allow us to forego underscores in package names, which are recommended against). What are the implications
of this on extensability? If this is being designed with essentially a micro-service architecture, and to allow replacement of any given component, is it better to
use different namespaces and consider each of these a totally different, separate thing?
