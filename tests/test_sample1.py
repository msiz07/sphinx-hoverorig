import pytest

@pytest.fixture
def sample_fixture():
    return "output from sample_fixture"

def test_dummy(sample_fixture):
    assert sample_fixture == "output from sample_fixture"
