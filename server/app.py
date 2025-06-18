from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods =['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_list = [message.to_dict() for message in messages]
        return make_response(jsonify(messages_list), 200)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_message = Message(
                body = data.get("body"),
                username = data.get("username"),
            )
            db.session.add(new_message)
            db.session.commit()
            return make_response(jsonify(new_message.to_dict()), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    
    if not message:
        return make_response({
            "message": "This message does not exist in our database."
        }, 404)
        
    if request.method == 'GET':
        return make_response(message.to_dict(), 200)
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr (message, attr, data.get(attr))
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
    return make_response({
        "delete_successful": True,
        "message": "message deleted"
    })

if __name__ == '__main__':
    app.run(port=5555)
