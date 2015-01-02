"""
Tests for version.py
"""
from rpymostat.version import VERSION
import re


class TestVersion:
    """
    Test version.py
    """

    def test_version(self):
        """
        test version constant
        """
        assert type(VERSION) == type('')
        m = re.match('^\d+\.\d+\.\d+$', VERSION)
        assert m is not None
