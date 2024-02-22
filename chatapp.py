
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

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form["message"]
    response = "Message received: " + message
    return response

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    messages_collection.insert_one({"message": message})
    return jsonify({'message': 'Message sent successfully'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = [msg["message"] for msg in messages_collection.find()]
    return jsonify({'messages': messages})

if __name__ == "__main__":
    app.run()