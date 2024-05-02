from flask import Flask, render_template, request
from flask_socketio import SocketIO
import datetime

#Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere' #This key should be a random string and it’s used for session handling.

#SocketIO
socketio = SocketIO(app)

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
    chat_messages = []
    return render_template('index.html', chat_messages=chat_messages) #chatroom.html !!!

#SocketIO event handler for new messages    
@socketio.on('message')
def handle_messages(data):
    user = data.get('user', 'New User')
    message = data['message']
    timestamp = datetime.datetime.now() #update
    
    #Broadcast the new message to all connected clients
    socketio.emit('new_message', {
        'user': user,
        'message': message,
        'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }, broadcast=True)
#server-socketio Flask app entry point    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True) #host='18.220.33.51', '127.0.0.1'
    