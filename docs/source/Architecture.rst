RaspberryPyMostat Architecture
==============================

High-Level Diagram
------------------

See `architecture.svg <architecture.svg>`__ for the actual file, or
`architecture.dia <architecture.dia>`__ for the
`Dia <https://wiki.gnome.org/Apps/Dia/>`__ source.

.. figure:: https://cdn.rawgit.com/jantman/RPyMostat/PoC/architecture.svg
   :alt: High-level SVG diagram of architecture

   High-level SVG diagram of architecture

Overview
--------

The architecture of RaspberryPyMostat is made up of four main
components:

-  The main control process, which handles the actual data evaluation,
   schedling and control decisions. This also connects directly to the
   databases, and provides a ReST API.
-  The web interface (desktop and mobile), currently planned to be
   Flask. This is a standalone "thing", which simply communicates with
   the main control process via its ReST API.
-  One (or more) physical control processes, which receive instructions
   from the main control process via a ReST API, and control relays (or
   whatever is needed to drive the actual HVAC equipment).
-  One or more temperature sensors, which send their results back to the
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