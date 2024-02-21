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
 
chat_messages = []
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    message = data.get('message')
    chat_messages.append({'sender': sender, 'recipient': recipient, 'message': message})
    return jsonify({'message': 'Message sent successfully'})

@app.route('/get_messages/<recipient>', methods=['GET'])
def get_messages(recipient):
    recipient_messages = [msg for msg in chat_messages if msg['recipient'] == recipient]
    return jsonify({'messages': recipient_messages})

if __name__ == "__main__":
    app.run()