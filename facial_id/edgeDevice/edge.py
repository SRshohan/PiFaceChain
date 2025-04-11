import socketio
import time
import RPi.GPIO as GPIO

# --- GPIO Setup ---
# Use BCM pin numbering. Change to GPIO.BOARD if needed.
GPIO.setmode(GPIO.BCM)
door_pin = 18  # Replace with the actual GPIO pin connected to the door actuator
GPIO.setup(door_pin, GPIO.OUT)
GPIO.output(door_pin, GPIO.LOW)  # Ensure the door is initially closed (or inactive)

# Create a SocketIO client instance.
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server.")

@sio.event
def disconnect():
    print("Disconnected from server.")
    GPIO.cleanup()  # Clean up GPIO on disconnect

# Event handler for the 'open_door' event sent by the server.
@sio.on('open_door')
def on_open_door(data):
    print("Received open_door command:", data)
    # Activate the GPIO pin to open the door.
    open_door()
    # After the door is opened, emit a door status event back to the server.
    sio.emit('door_status', {'status': 'door opened successfully', 'timestamp': time.time()})

def open_door():
    """
    Activate the GPIO pin to simulate opening the door.
    Adjust the pin number, timing, and hardware logic as needed.
    """
    print("Activating GPIO pin to open door...")
    GPIO.output(door_pin, GPIO.HIGH)
    # Keep the door activated for 2 seconds (simulate the door open duration)
    time.sleep(2)
    GPIO.output(door_pin, GPIO.LOW)
    print("Door action complete. GPIO pin deactivated.")

if __name__ == '__main__':
    # Replace 'http://server_ip:5000' with your actual server address.
    sio.connect('http://192.168.1.14:5000')
    # Wait for events indefinitely.
    sio.wait()
