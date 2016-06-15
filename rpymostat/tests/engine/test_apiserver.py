"""
Tests for runner.py
"""
import sys
from klein import Klein

from rpymostat.engine.apiserver import APIServer, server
from rpymostat.version import VERSION

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, MagicMock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, MagicMock, DEFAULT  # noqa

pbm = 'rpymostat.engine.apiserver'
pb = '%s.APIServer' % pbm


class TestAPIServer:

    def test_init(self):
        mock_mongo = Mock()
        mock_klein = Mock(spec_set=Klein)
        APIServer.app = mock_klein
        with patch.multiple(
            pbm,
            APIv1=DEFAULT,
        ) as mocks:
            cls = APIServer(mock_mongo)
        assert cls.app == mock_klein
        assert server.version == 'RPyMostat %s' % VERSION
        assert mocks['APIv1'].mock_calls == [
            call(cls, mock_klein, []),
            call().setup_routes()
        ]
        assert cls.dbconn == mock_mongo

    def test_root(self):
        """
        test root()
        """
        req_mock = Mock()
        mock_mongo = Mock()
        mock_klein = MagicMock(spec_set=Klein)
        with patch('rpymostat.engine.apiserver.Klein', mock_klein):
            cls = APIServer(mock_mongo)
        assert cls.handle_root(cls, req_mock) == 'Hello, World!'
