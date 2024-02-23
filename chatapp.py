
from flask import Flask, render_template, request, jsonify      #Imports necessary modules from Flask for creating a web application and handling requests
from pymongo import MongoClient     #Imports the MongoClient class from pymongo for interacting with MongoDB

app = Flask(__name__)   #Creates a Flask application instance
client = MongoClient("your_mongodb_connection_string")  #Establishes a connection to MongoDB Atlas using the provided connection string
db = client["chat_app"] #Accesses the "chat_app" database in MongoDB Atlas
messages_collection = db["messages"]    #Accesses the "messages" collection within the "chat_app" database

@app.route("/", methods=["GET", "POST"])    #Decorator that defines a route for both GET and POST requests to the root URL
def home(): #Defines the view function for the "/" route
    if request.method == "GET": #Checks if the request method is GET
        return render_template("index.html")    #Renders the "index.html" template for GET requests
    if request.method == "POST":    #Checks if the request method is POST
        text = request.form.get('textbox')  #Retrieves the text input from the form field named 'textbox'
        # Process the text if needed
        return render_template("index.html", output=process_text(text), user_text=text) #Renders the template with processed text and the original user input

@app.route('/chat', methods=['POST'])   #Decorator that defines a route '/chat' which only accepts POST requests
def chat():     #Defines the view function for the '/chat' route
    message = request.form["message"]   #Retrieves the 'message' data from the POST request form
    response = "Message received: " + message   #Creates a response message indicating that the message was received
    return response     #Returns the response message to the client

@app.route('/send_message', methods=['POST'])   #Decorator for the '/send_message' route that accepts POST requests
def send_message():     #Defines the view function for sending messages
    data = request.get_json()   #Retrieves JSON data from the request
    message = data.get('message')   #Extracts the 'message' field from the JSON data
    messages_collection.insert_one({"message": message})    #Inserts the message into the 'messages_collection' in MongoDB
    return jsonify({'message': 'Message sent successfully'})    #Returns a JSON response indicating successful message transmission

@app.route('/get_messages', methods=['GET'])    #Decorator for the '/get_messages' route that only accepts GET requests
def get_messages(): #Defines the view function for fetching messages
    messages = [msg["message"] for msg in messages_collection.find()]   #Retrieves all messages from the 'messages_collection' in MongoDB
    return jsonify({'messages': messages})      #Returns a JSON response containing all messages fetched

if __name__ == "__main__":      #Checks if the script is being run directly
    app.run()       #Starts the Flask application when the script is executed directly