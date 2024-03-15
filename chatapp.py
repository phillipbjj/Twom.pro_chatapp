from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import datetime

#Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere' #This key should be a random string and it’s used for session handling.

#test commit
#MongoDB Client
uri = "mongodb+srv://pjdempsey3:Ilovebjj123@twomprochat.ncz4mxt.mongodb.net/?retryWrites=true&w=majority&appName=Twomprochat"
client = MongoClient(uri, server_api=ServerApi('1'))
chat_db = client['ChatData']
message_collection = chat_db['messageData']
user_collection = chat_db['userData']
msgtime_collection = chat_db['timestampData']

#SocketIO
socketio = SocketIO(app)
#chat_messages = []

#This is defining the route for your main page. When someone visits your website, the index function gets called. 
@app.route('/', methods=['GET', 'POST'])
def index(): #The index() function renders the index.html template, which will include the chat room interface
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # Handle form submission or other POST requests!!!
        # You can access form data using request.form.get('field_name')!!!
        pass

#Route for the chat room
@app.route('/chatroom', methods=['GET'])
def chatroom(): #The chat() function retrieves the chat messages from the MongoDB collection and renders the chat.html template with the messages
    #Retrieve chat messages from the database or cache
    chat_messages = list(message_collection.find().sort("timestamp", -1))
    return render_template('index.html', chat_messages=chat_messages) #chatroom.html !!!

#SocketIO event handler for new messages    
@socketio.on('message')
def handle_messages(data):
    user = data.get('user', 'New User')
    message = data['message']
    timestamp = datetime.datetime.now()
    
    #Before saving, checks if the user exists in the userData collection, if not it adds to the userData collection.
    user = user_collection.find_one({'user': user})
    if not user:
        user_collection.insert_one({'username': user})
        
    #Save the message to MongoDB
    message_collection.insert_one({ 
        'user': user,
        'message': message,
        'timestamp': timestamp
    })  
    #Broadcast the new message to all connected clients
    emit('new_message', {
        'user': user,
        'message': message,
        'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }, broadcast=True)
#server-socketio Flask app entry point    
if __name__ == '__main__':
    socketio.run(app(debug=True))