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

class TestApp:
    '''Flask application in app.py'''

    def test_has_correct_columns(self, setup_db):
        with app.app_context():
            # Create a test message
            test_message = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(test_message)
            db.session.commit()

            # Query the message
            m = Message.query.filter(
                Message.body == "Hello 👋"
            ).filter(Message.username == "Liza")

            # Verify the message exists and has the correct columns
            assert m.count() == 1
            message = m.first()
            assert hasattr(message, 'created_at')
            assert hasattr(message, 'updated_at')
            assert isinstance(message.created_at, datetime)
            assert isinstance(message.updated_at, datetime)

            # Clean up
            db.session.delete(message)
            db.session.commit()

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():

            app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():

            response = app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            assert(response.content_type == 'application/json')

            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()


    def test_updates_body_of_message_in_database(self, setup_db):
        '''updates the body of a message in the database.'''
        with app.app_context():
            # Create a test message
            test_message = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(test_message)
            db.session.commit()

            # Get the message
            m = Message.query.first()
            id = m.id
            body = m.body

            app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            g = Message.query.filter_by(body="Goodbye 👋").first()
            assert(g)

            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self, setup_db):
        '''returns data for the updated message as JSON.'''
        with app.app_context():
            # Create a test message
            test_message = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(test_message)
            db.session.commit()

            # Get the message
            m = Message.query.first()
            id = m.id
            body = m.body

            response = app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Goodbye 👋")

            g = Message.query.filter_by(body="Goodbye 👋").first()
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)