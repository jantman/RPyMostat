Service Discovery
=================

There are a few options out there for service discovery. I'm only considering ones that are cross-platform and language-agnostic,
so this pretty much means [DNS-SD](http://en.wikipedia.org/wiki/Zero-configuration_networking#DNS-SD) or [SLP](http://en.wikipedia.org/wiki/Service_Location_Protocol).

python-zeroconf
----------------

[python-zeroconf](https://github.com/jstasiak/python-zeroconf) appears to be the current winner.

* Native pure-python implementation; no annoying ctypes or external dependencies
* hosted on pypi
* an actual package, complete with tests (TravisCI) and coverage reports
* Little to no logging; I have a [branch](https://github.com/jantman/python-zeroconf/tree/more_logging) that fixes this and a few other things
* re-registration of services seems broken (see [issue 16](https://github.com/jstasiak/python-zeroconf/issues/16)) as does responding to requests
* the examples actually run; I got them working on 2 separate machines, but only if the browser was started *before* the registration happened
* some issues around logging (see [issue 15](https://github.com/jstasiak/python-zeroconf/issues/15))
* updated relatively recently
* Need to see if this will run in Twisted, or if I'd just run it as a separate process or thread...

pybonjour
---------

[pybonjour](https://code.google.com/p/pybonjour/) is one option, but it has a lot of drawbacks

* the example code dies for me with mysterious, meaningless exceptions
* not Python3 compatible; there's a [fork](https://github.com/depl0y/pybonjour-python3) that is, but its examples don't even work under python3
* no testing
* download isn't actually hosted on pypi
* seems relatively abandoned
* depends on Avahi's bonjour compatibility libs, or Bonjour, depending on platform

Avahi Bindings
---------------

[Avahi's official bindings](http://avahi.org/wiki/Bindings)

* they're stable, because they're used by Avahi itself
* testing would be a pain, because they require a bunch of libraries like DBUS and Avahi itself
* uses Avahi over DBUS - doesn't do things itself, and requires Avahi to be running
* massive external dependencies, no real package

Other Options
--------------

* [anyMesh](https://github.com/AnyMesh/anyMesh-Python) - A multi-platform, decentralized, auto-discover and auto-connect mesh networking and messaging API
* Twisted and UDP multicast?
* [python-brisa UPnP framework](http://brisa.garage.maemo.org/doc/html/upnp/ssdp.html) SSDP Server
* [mdns](https://github.com/svinota/mdns) - Python, no docs, no readme
* [txbonjour](https://github.com/jdcumpson/txbonjour) - a Twisted plugin for Bonjour; looks simple, it might be the right thing if it works - based on pybonjour, so probably a no-go
