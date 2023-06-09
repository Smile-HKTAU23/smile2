from flask import Flask, request
from flask_socketio import SocketIO

from logic import dummy_finder, parse_details, get_driver_route
from db import SmileDB, DB_FILENAME, Location, LocationWithName

api = Flask(__name__)
api.config['SECRET_KEY'] = 'secret_key'
db = SmileDB(DB_FILENAME)
socketio = SocketIO(api, cors_allowed_origins="*")

# Demo
DEMO_MODE = True
DEMO_COUNTER = 0
DEMO_CHOSEN_COURSE_INDEX = 0
DEMO_PASSENGER = {'passenger': {'source': {'lat': 32.069235, 'lng': 34.825947, 'name': "Shlomtsiyon 13-1 Ramat Gan"},
                                'destination': {'lat': 32.1140370, 'lng': 34.805650,
                                                'name': "ANU Museum of the Jewish People"}}}


def demo_populate_passenger_locations():
    chosen = db.get_courses()[DEMO_CHOSEN_COURSE_INDEX]
    # TODO: Get name of demo pickup and dropoff
    passenger_source_name = DEMO_PASSENGER["passenger"]["source"]["name"]
    passenger_dest_name = chosen["destination"]["name"]
    route = get_driver_route(passenger_source_name, passenger_dest_name)
    route = route[::5]
    return route


def demo_populate_driver_locations():
    chosen = db.get_courses()[DEMO_CHOSEN_COURSE_INDEX]
    route = get_driver_route(chosen["source"]["name"], chosen["destination"]["name"])
    route = route[::5]
    return route


DEMO_DRIVER_LOCATIONS = demo_populate_driver_locations()
DEMO_PASSENGER_LOCATIONS = demo_populate_passenger_locations()


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
        details.update(DEMO_PASSENGER)
    print(f'I: {details}')
    options = logic_get_options(details)
    print(f'O: {options}')
    pos = {'lat': float(request.args.get("source_lat")), 'lng': float(request.args.get("source_lng"))}
    result = {'options': options, 'pos': pos}
    print(result)
    return result


@socketio.on('message')
def handle_message(message):
    global DEMO_COUNTER
    if DEMO_MODE:
        DEMO_COUNTER += 1
        driver_location = DEMO_DRIVER_LOCATIONS[DEMO_COUNTER % len(DEMO_DRIVER_LOCATIONS)]
        driver_location = {'lat': driver_location[0], 'lng': driver_location[1]}
        passenger_location = DEMO_PASSENGER_LOCATIONS[DEMO_COUNTER % len(DEMO_PASSENGER_LOCATIONS)]
        passenger_location = {'lat': passenger_location[0], 'lng': passenger_location[1]}
        passenger_destination = DEMO_PASSENGER["passenger"]["destination"]

    else:
        # Get driver location and return it.
        raise NotImplementedError()

    socketio.emit('response', {"driver_location": driver_location,
                               "passenger_location": passenger_location,
                               "passenger_destination": passenger_destination})


if __name__ == "__main__":
    socketio.run(api, debug=True)
