Twisted for RPyMostat
======================

This documents my initial tests for using [Twisted](https://twistedmatrix.com/) as the framework for the main/hub process.

Twisted Basics
---------------

* [Reactors](https://twistedmatrix.com/documents/current/core/howto/reactor-basics.html)
* [Spawning Processes](https://twistedmatrix.com/documents/current/core/howto/process.html)
* [Deferreds](https://twistedmatrix.com/documents/current/core/howto/defer-intro.html); [Deferred Reference](https://twistedmatrix.com/documents/current/core/howto/defer.html)
* [Writing Servers](https://twistedmatrix.com/documents/current/core/howto/servers.html)
* [Scheduling](https://twistedmatrix.com/documents/current/core/howto/time.html) - "run in X seconds" or "run every N seconds"
* [Threading](https://twistedmatrix.com/documents/current/core/howto/threading.html) - "most code in Twisted is not thread-safe"
* [Application Framework](https://twistedmatrix.com/documents/current/core/howto/application.html) - seems like this might be too baisc for my needs?
* [Logging](https://twistedmatrix.com/documents/current/core/howto/logging.html#using-the-standard-library-logging-module) using the logging module, and capturing Twisted's internal messages; note this can block logging

The more I read about this, the more I think Twisted is probably *not* the solution I need (I seem to need _real_ threading or multiprocessing, not just async network IO). i.e. see
this really important FAQ, [Why does it take a long time for data I send with transport.write to arrive at the other side of the connection?](http://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#WhydoesittakealongtimefordataIsendwithtransport.writetoarriveattheothersideoftheconnection).


Third-Party Twisted Modules
----------------------------

* [Paisley](https://launchpad.net/paisley) CouchDB client
* [sAsync](https://pypi.python.org/pypi/sAsync/0.7) Async SQLAlchemy
* [TxScheduling](https://github.com/benliles/TxScheduling) cron-like scheduling
* [txAMQP](https://launchpad.net/txamqp)
* [txrdq](https://launchpad.net/txrdq) resizable dispatch queue

ReST API
---------

* we need to serve it nicely (not a horrible hack)
* read/write from database used by other threads (DB tech still unknown; maybe flat files for now?)
* read/write to some shared global memory (or main thread)

### Links

* [web development with Twisted](http://twistedmatrix.com/trac/wiki/WebDevelopmentWithTwisted)
* [web services with twisted](http://zenmachine.wordpress.com/web-services-and-twisted/)
* [Building RESTful, Service-Oriented Architectures with Twisted](http://lanyrd.com/2012/pycon-za/syyfm/) video and slide deck
* [Twisted community code and add-ons](https://twistedmatrix.com/trac/wiki/ProjectsUsingTwisted)
* [Klein](http://klein.readthedocs.org/en/latest/) a web micro-framework
* [Going asynchronous: from Flask to Twisted Klein](http://tavendo.com/blog/post/going-asynchronous-from-flask-to-twisted-klein/)

Signals
--------

* Signals or some other sort of notification mechanism

Scheduling
-----------

* Scheduled tasks

Testing
--------

* test-ability (i.e. pytest, possibly something else to test the threading/network)

### Links

* [pytest-twisted](https://pypi.python.org/pypi/pytest-twisted)
* [Twisted TDD/Trial docs](https://twistedmatrix.com/documents/14.0.0/core/howto/trial.html)
* [TwistedTrial](http://twistedmatrix.com/trac/wiki/TwistedTrial)
* [Unit Tests in Twisted](http://twistedmatrix.com/documents/14.0.0/core/development/policy/test-standard.html) (internal to Twisted itself)
* [some notes](http://www.mechanicalcat.net/richard/log/Python/Tips_for_Testing_Twisted) on using nose to test Twisted
* Random selection of GitHub projects using pytest-twisted: [scrapy](https://github.com/scrapy/scrapy), [pyrake](https://github.com/elkingtowa/pyrake), [snappy](https://github.com/russell/snappy/blob/master/snappy/tests/test_webserver.py), [pokerthproto](https://github.com/FlorianWilhelm/pokerthproto/blob/master/tests/test_protocol.py), [mcloud](https://github.com/modera/mcloud)
