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
                body="Hello World",
                username="Liza"
            )
            db.session.add(test_message)
            db.session.commit()

            # Verify the message properties
            assert test_message.body == "Hello World"
            assert test_message.username == "Liza"
            assert isinstance(test_message.created_at, datetime)
            assert isinstance(test_message.updated_at, datetime)

            # Clean up
            db.session.delete(test_message)
            db.session.commit()
