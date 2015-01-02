Twisted for RPyMostat
======================

This documents my initial tests for using [Twisted](https://twistedmatrix.com/) as the framework for the main/hub process.

First, a really good [basic doc on Deferreds](http://ezyang.com/twisted/defer2.html) and a [not-so-short introduction to Asynchronous programming](http://krondo.com/blog/?p=1209).

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

Klein
------

### Links

* [some](https://github.com/SamuelMarks/cscie90-hw8/blob/baae8d648420c2cd8c07391a5bc425152a996af1/hw8/server.py) [other](https://github.com/rackerlabs/otter/blob/master/otter/rest/application.py) [projects](https://github.com/rackerlabs/otter/blob/master/otter/rest/otterapp.py) [appear](https://github.com/rackerlabs/otter/blob/master/otter/rest/admin.py) [to](https://github.com/therve/ersid/blob/1bc409851ee104ccef22ff4835daa00cdb29a8c2/ersid/rest.py) [use](https://github.com/armooo/jukebox/blob/24e41bb2d20aff6859c7133ca4d7fc37ad3eaba5/jukebox/httpd.py) [klein](https://github.com/radix/coverapi/blob/7611797095c5ffd35f21363bd7cdc4150c15fd6a/coverapi/httpapi.py) (in non-trivial ways)
* [this blog post](http://tavendo.com/blog/post/mixing-web-and-wamp-code-with-twisted-klein/) was actually VERY helpful

Signals
--------

* Signals or some other sort of notification mechanism

### Links

* [helga](https://github.com/shaunduncan/helga) uses [smokesignal](https://github.com/shaunduncan/smokesignal) quite nicely

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
* Interestingly, I can't find _anything_ on GitHub that uses pytest-twisted's `pytest.blockon`. `pytest.inlineCallbacks` is used by a number of mcloud [tests](https://github.com/modera/mcloud/blob/c5adea19b05c71d8dc76487112e034e57b703fd1/tests/test_txhttp.py), [jukebox](https://github.com/armooo/jukebox/blob/fc6322c05c67bc96566500d0edeb0a988cbcf19c/test/test_storage.py), [webmonitor](https://github.com/eddwardo/webmonitor/blob/529a0cacaf60f1d9a1acf1decef50ef0fa93e543/tests/test_monitor.py) and [spiral](https://github.com/habnabit/spiral/blob/060dbf90fee1d1bbc9905f9d2a5e6667f2eb89b2/spiral/test/test_acceptance.py)
