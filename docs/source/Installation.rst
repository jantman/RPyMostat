RPyMostat Installation, Configuration and Usage
================================

Requirements
------------

* Python 2.7 or 3.3+ (currently tested with 2.7, 3.3, 3.4, 3.5)
* Python `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)
* MongoDB (developed against 2.4, which is available in the Debian and Raspbian repos)

Installation
------------

It's recommended that you install into a virtual environment (virtualenv /
venv). See the `virtualenv usage documentation <http://www.virtualenv.org/en/latest/>`_
for information on how to create a venv. If you really want to install
system-wide, you can (using sudo).

.. code-block:: bash

    pip install rpymostat

Configuration
-------------

The RPyMostat Engine is configured solely via environment variables. This is intended
to make it simple to run at the command line, as a system service, or in a container.

Usage
-----

Something.
