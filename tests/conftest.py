from src.defang_api.servelocal import run
import pytest

@pytest.fixture
def app():
    app = run()
    return app