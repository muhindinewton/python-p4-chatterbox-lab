from app import app
from models import db

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create tables with the correct schema
        db.create_all()

if __name__ == '__main__':
    init_db()
