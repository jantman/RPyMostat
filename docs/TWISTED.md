Twisted for RPyMostat
======================

This documents my initial tests for using [Twisted](https://twistedmatrix.com/) as the framework for the main/hub process.

ReST API
---------

* we need to serve it nicely (not a horrible hack)
* read/write from database used by other threads (DB tech still unknown; maybe flat files for now?)
* read/write to some shared global memory (or main thread)

Signals
--------

* Signals or some other sort of notification mechanism

Scheduling
-----------

* Scheduled tasks

Testing
--------

* test-ability (i.e. pytest, possibly something else to test the threading/network)

