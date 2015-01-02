"""
RPyMostat test support / fixtures
"""

import pytest
import logging
from mock import MagicMock


@pytest.fixture
def mocklogger():
    ml = MagicMock(name='mocklogger', spec_set=logging.Logger)
    return ml
