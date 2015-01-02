"""
Tests for runner.py
"""
from mock import patch, call, MagicMock
from klein import Klein

from rpymostat.tests.support import mocklogger
from rpymostat.hub.apiserver import HubAPIServer
from twisted.web.server import Request


class TestHubAPIServerMocked:
    """
    Tests the hub APIServer functions with mocked objects; no actual Twisted testing
    """

    def test_root(self):
        """
        test root()
        """
        req_mock = MagicMock(spec_set=Request)
        mock_klein = MagicMock(spec_set=Klein)
        with patch('rpymostat.hub.apiserver.Klein', mock_klein):
            hapi = HubAPIServer()
            res = hapi.root(req_mock)
        assert res == "Hello, World!"

    def test_paramed_url(self):
        """
        test paramed_url()
        """
        req_mock = MagicMock(spec_set=Request)
        mock_klein = MagicMock(spec_set=Klein)
        with patch('rpymostat.hub.apiserver.Klein', mock_klein):
            hapi = HubAPIServer()
            res = hapi.paramed_url(req_mock, 'foobar')
        assert res == "Got param 'foobar' in argument"
