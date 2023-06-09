from flask import Flask, request
from flask_socketio import SocketIO

from logic import dummy_finder, parse_details
from db import SmileDB, DB_FILENAME, Location, LocationWithName

api = Flask(__name__)
api.config['SECRET_KEY'] = 'secret_key'
db = SmileDB(DB_FILENAME)
socketio = SocketIO(api, cors_allowed_origins="*")

# Demo
DEMO_MODE = True
DEMO_DRIVER_LOCATIONS = [{'lat': 0, 'lon': 0}]
DEMO_COUNTER = 0


def logic_get_options(details):
    src_coor, dst_coor, drivers_rout_dict = parse_details(details)
    result = dummy_finder(drivers_rout_dict, src_coor, dst_coor)
    return result


@api.route('/get_options')
def get_options():
    courses = db.get_courses()

    details = {"passenger": {"source": {"lat": float(request.args.get("source_lat")),
                                        "lng": float(request.args.get("source_lng")),
                                        "name": request.args.get("source_name")},
                             "destination": {"lat": float(request.args.get("dest_lat")),
                                             "lng": float(request.args.get("dest_lng")),
                                             "name": request.args.get("dest_name")}},
               "courses": courses}
    if DEMO_MODE:
        demo_location = {'passenger': {'source': {'lat': 32.069235, 'lng': 34.825947, 'name': "Sholmzion Ramat Gan"},
                      'destination': {'lat': 32.113169, 'lng': 34.804345, 'name': "Tel Aviv University"}}}
        details.update(demo_location)
    print(f'I: {details}')
    options = logic_get_options(details)
    print(f'O: {options}')
    pos = {'lat': float(request.args.get("source_lat")), 'lng': float(request.args.get("source_lng"))}
    result = {'options': options, 'pos': pos}
    print(result)
    return result


@socketio.on('message')
def handle_message(message):
    print('Received:', message)
    if DEMO_MODE:
        DEMO_COUNTER += 1
        location = DEMO_DRIVER_LOCATIONS[DEMO_COUNTER % len(DEMO_DRIVER_LOCATIONS)]
    else:
        # Get driver location and return it.
        raise NotImplementedError()

    socketio.emit('response', {"driver_location": location})

if __name__ == "__main__":
    socketio.run(api, debug=True)
