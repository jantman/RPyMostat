"""
Tests for runner.py
"""
import logging
import sys
from contextlib import nested

from mock import patch, call, MagicMock
from klein import Klein
from twisted.web.server import Site

from rpymostat.tests.support import mocklogger
from rpymostat import runner
from rpymostat.hub.apiserver import HubAPIServer


class TestRunnerMocked:
    """
    Tests the runner functions with mocked objects; no actual Twisted testing
    """

    def test_main(self, mocklogger):
        """
        test main function
        """
        with nested(
                patch('logging.getLogger'),
                patch('rpymostat.runner.run', autospec=True),
                patch('twisted.python.log.startLogging', autospec=True),
        ) as (mock_getlogger, mock_run, mock_tlog):
            mock_getlogger.return_value = mocklogger
            runner.main()
        assert mock_getlogger.call_count == 1
        assert mocklogger.setLevel.call_args_list == [call(logging.DEBUG)]
        assert mocklogger.debug.call_args_list == [
            call("starting twisted logging"),
            call("calling run()"),
            call("run() returned")
            ]
        assert mock_tlog.call_args_list == [call(sys.stdout)]
        assert mock_run.call_count == 1

    def test_run(self, mocklogger):
        """
        test run()
        """
        mock_hapi_obj = MagicMock(spec_set=HubAPIServer)
        mock_hapi_obj.app = MagicMock(spec_set=Klein)
        resource_mock = MagicMock()
        mock_hapi_obj.app.resource.return_value = resource_mock
        mock_site_obj = MagicMock(spec_set=Site)
        with nested(
                patch('logging.getLogger'),
                patch('rpymostat.runner.reactor', autospec=True),
                patch('rpymostat.runner.HubAPIServer', autospec=True),
                patch('rpymostat.runner.Site', autospec=True),
        ) as (mock_getlogger, mock_reactor, mock_hapi, mock_site):
            mock_hapi.return_value = mock_hapi_obj
            mock_getlogger.return_value = mocklogger
            mock_site.return_value = mock_site_obj
            runner.run()
        assert mock_getlogger.call_count == 1
        assert mocklogger.setLevel.call_args_list == [call(logging.INFO)]
        assert mocklogger.debug.call_args_list == [
            call("instantiating apiserver"),
            call("reactor.listenTCP"),
            call("reactor.run()"),
            call("finished")
            ]
        assert mock_hapi.mock_calls == [call(), call().app.resource()]
        assert mock_hapi_obj.mock_calls == [call.app.resource()]
        assert mock_site.mock_calls == [call(resource_mock)]
        assert mock_reactor.listenTCP.call_args_list == [
            call(8088, mock_site_obj)
            ]
        assert mock_reactor.run.call_args_list == [
            call()
            ]
