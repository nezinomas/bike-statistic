import pytest
import tempfile


@pytest.fixture(scope="session", autouse=True)
def temp_folder_for_cash(tmpdir_factory):
    with tempfile.TemporaryDirectory() as CASH_ROOT:
        pass
