import pytest

@pytest.fixture
def fake_dependent(**kwargs):
    return 'fake dependent'

class FakeDependentWhichIsAClass:
    pass

@pytest.fixture
def fake_dependent_which_is_a_class(pytest_request, **kwargs):
    return FakeDependentWhichIsAClass
