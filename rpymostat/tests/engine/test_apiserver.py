"""
Tests for runner.py
"""
import sys
from klein import Klein

from rpymostat.engine.apiserver import APIServer
# from twisted.web.server import Request

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, MagicMock  # noqa
else:
    from unittest.mock import patch, MagicMock  # noqa


class DONOTTestAPIServerMocked:
    """
    Tests the hub APIServer functions with mocked objects;
    no actual Twisted testing.
    """

    def test_root(self):
        """
        test root()
        """
        # req_mock = MagicMock(spec_set=Request)
        mock_klein = MagicMock(spec_set=Klein)
        with patch('rpymostat.engine.apiserver.Klein', mock_klein):
            APIServer()
