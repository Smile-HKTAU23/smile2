from flask import Flask, request
from flask_socketio import SocketIO

from db import SmileDB, DB_FILENAME, Location

api = Flask(__name__)
api.config['SECRET_KEY'] = 'secret_key'
db = SmileDB(DB_FILENAME)
socketio = SocketIO(api, cors_allowed_origins="*")

# Demo
DEMO_DRIVER_LOCATIONS = [{'lat': 0, 'lon': 0}]
DEMO_COUNTER = 0
DEMO_MODE = False

def logic_get_options(passenger_source: Location,
                      passenger_destination: Location,
                      courses):
    print("logic_get_options() is a mock - returning first courses...")
    result = [{"id": c.id, 'pickup': {'lat': 0, 'lon': 0}, 'dropoff': {'lat': 0, 'lon': 0}}
              for c in courses]
    return result


@api.route('/get_options')
def get_options():
    courses = db.get_courses()
    source = Location(lat=request.args.get("source_lat"),
                      lon=request.args.get("source_lon"))
    destination = Location(lat=request.args.get("dest_lat"),
                      lon=request.args.get("dest_lon"))

    options = logic_get_options(passenger_source=source,
                                passenger_destination=destination,
                                courses=courses)
    print(options)
    return options


@socketio.on('message')
def handle_message(message):
    print('Received:', message)  
    if DEMO_MODE:
        DEMO_COUNTER += 1
        location = DRIVER_LOCATIONS[DEMO_COUNTER % len(DEMO_DRIVER_LOCATIONS)]
    else:
        # Get driver location and return it.
        raise NotImplementedError()

    socketio.emit('response', {"driver_location": location})

if __name__ == "__main__":
    socketio.run(api, debug=True)
