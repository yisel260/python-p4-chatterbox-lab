from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods= ['GET','POST'])
def messages():
    messages= Message.query.order_by(asc(Message.created_at)).all()
    
    if request.method == 'GET': 
            
        messages_serialized= []
        for message in messages:
            message_dict= message.to_dict()
            messages_serialized.append(message_dict)
        
        response = make_response(
            messages_serialized,
            200)

        return (response)
    elif request.method=='POST':

        username = request.json['username']
        body = request.json['body']

        new_message = Message(
            username= username,
            body= body
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()
        response = make_response(
            new_message_dict,
            201)
        return response


@app.route('/messages/<int:id>', methods=['GET','PATCH','DELETE'])
def messages_by_id(id):    

    message= Message.query.filter(Message.id == id).first()

    if message == None: 
            response_body={ 
               "message": "This record does not exist in our database. Please try again."
                }
            response = make_response(response_body, 404)

            return response
    else: 
        if request.method == "GET": 
            message_serialized = message.to_dict()
            return make_response ( message_serialized, 200  )
        
        elif request.method == 'PATCH':

            message.body = request.json['body']
            
            db.session.add(message)
            db.session.commit()

            message_dict = message.to_dict()

            response = make_response(
                 message_dict,
                 200) 
            return response
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response



if __name__ == '__main__':
    app.run(port=5555)
