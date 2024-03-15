import socketio

# Create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# Define event handlers
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def handle_messages(sid, data):
    sio.emit('chat message', data)

# Run the Socket.IO server
if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)