from flask import Flask, render_template, request, jsonify
import backend

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        text = request.form.get('textbox')
        return render_template("index.html", output = backend.twompro_chatapp(float(text)), user_text = text)
    
@app.route('/chat', methods=['POST'])    
def chat():                             
    message = request.form["message"]   
    response = "Message received hehe :3: " + message
    return response   
 

# Update the send_message endpoint to store messages in the database
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    # Store the message in the database instead of chat_messages list
    # Insert the message into the database table for chat messages
    # Example: db.insert_message(message)
    return jsonify({'message': 'Message sent successfully'})

# Modify the get_messages endpoint to return all messages for the global chat
@app.route('/get_messages', methods=['GET'])
def get_messages():
    # Retrieve all messages from the database
    # Example: messages = db.get_all_messages()
    # Return all messages as JSON
    return jsonify({'messages': messages})

if __name__ == "__main__":
    app.run()