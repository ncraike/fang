
import unittest.mock

import pytest

# Module under test:
from fang.dependency_register import DependencyRegister

@pytest.fixture(scope='function')
def dep_reg():
    return DependencyRegister()

@pytest.fixture(scope='function')
def mock_dep_reg():
    return unittest.mock.NonCallableMock(
            spec=DependencyRegister())

@pytest.fixture(scope='function')
def fake_resource_name():
    return 'fake resource name'

@pytest.fixture(scope='function')
def fake_dependent():
    return 'fake dependent'
