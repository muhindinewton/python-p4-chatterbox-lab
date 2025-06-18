from datetime import datetime
import pytest
from app import app
from models import db, Message

@pytest.fixture(autouse=True)
def setup_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create tables with the correct schema
        db.create_all()
        yield
        # Clean up after tests
        db.session.remove()
        db.drop_all()

class TestMessage:
    '''Message model in models.py'''

    def test_has_correct_columns(self, setup_db):
        with app.app_context():
            # Create a test message
            test_message = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(test_message)
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)
