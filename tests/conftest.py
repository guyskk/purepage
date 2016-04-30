from purepage import create_app, db
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.yield_fixture(scope="session")
def app():
    app = create_app("purepage.config_test")
    db.load_designs(db, "design")
    yield app
    db.delete()
