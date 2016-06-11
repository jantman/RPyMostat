RaspberryPyMostat Architecture
==============================

Overview
--------

The architecture of RaspberryPyMostat is made up of four main
components:

-  Engine - the main control process, which handles the actual data evaluation,
   schedling and control decisions. This also connects directly to the
   databases, and provides a ReST API.
-  UI - The web interface (desktop and mobile), currently planned to be
   Flask. This is a standalone "thing", which simply communicates with
   the main control process via its ReST API.
-  Control - One (or more) physical control processes, which receive instructions
   from the main control process via a ReST API, and control relays (or
   whatever is needed to drive the actual HVAC equipment).
-  Sensor - One or more temperature sensors, which send their results back to the
   main control process via its ReST API.

While the typical implementation will likely place all of these
components on a RaspberryPi (single host deployment), this is by no
means a requirement. Each of the three non-main services (web UI,
physical control and temperature sensors) are completely independent.
They detect the master control process via
`DNS-SD <http://en.wikipedia.org/wiki/Zero-configuration_networking#DNS-SD>`__
meaning that they can live on different machines on the same LAN, and
find each other without any manual configuration.

All of the separate components communicate with each other over ReST
APIs, meaning that temperature inputs, physical control outputs, and web
interfaces can be replaced with any third-party code that conforms to
the API.
