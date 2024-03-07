from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import datetime

#Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere' #This key should be a random string and it’s used for session handling.


#MongoDB Client
uri = "mongodb+srv://pjdempsey3:<Ilovebjj123>@twomprochat.ncz4mxt.mongodb.net/?retryWrites=true&w=majority&appName=Twomprochat"
client = MongoClient(uri, server_api=ServerApi('1'))
chat_db = client['ChatData']
message_Collection = chat_db['messageData']
user_collect = chat_db['userData']
msgtime_collection = chat_db['timestampData']

#SocketIO
socketio = SocketIO(app)
chat_messages = []

#This is defining the route for your main page. When someone visits your website, the index function gets called. 
@app.route('/')
def index():
    return render_template('index.html')

#Route for the chat room
@app.route('/chat')
def chat():
    #Retrieve chat messages from the database or cache
    chat_messages = list(message_Collection.find().sort("timestamp", -1))
    return render_template('chat.html', chat_messages=chat_messages)

#SocketIO event handler for new messages    
@socketio.on('message')
def handle_message(data):
    message = data['message']
    sender = data.get('sender', 'Anonymous')
    timestamp = datetime.datetime.now()
    
    # Save the message to MongoDB
    message_Collection.insert_one({
        'sender': sender,
        'content': message,
        'timestamp': timestamp
    })
    
    # Broadcast the new message to all connected clients
    emit('new_message', {
        'sender': sender,
        'message': message,
        'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }, broadcast=True)
    
if __name__ == '__main__':
    socketio.run(app)