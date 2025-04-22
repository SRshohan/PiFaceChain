from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# Secret key for session management, adjust as needed
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# Route to trigger the door open command
@app.route('/open')
def open_door_command():
    # Emit the 'open_door' event to all connected clients (the Raspberry Pi)
    socketio.emit('open_door', {'command': 'open'})
    return "Door open command sent"

# Event handler for receiving door status from the edge device
@socketio.on('door_status')
def handle_door_status(data):
    print("Received door status:", data)
    # Here you can process the status 
    emit('status_received', {'response': 'Status received by server'})

if __name__ == '__main__':
    # Run the server on all interfaces, port 5000
    socketio.run(app, host='149.61.245.217', port=5000, debug=True)




