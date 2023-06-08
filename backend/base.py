from flask import Flask, request

from db import SmileDB, DB_FILENAME, Location

api = Flask(__name__)
db = SmileDB(DB_FILENAME)


def logic_get_options(passenger_source: Location,
                      passenger_destination: Location,
                      courses):
    print("logic_get_options() is a mock - returning first courses...")
    result = [{"id": c.id, 'pickup': {'lat': 31.0461, 'lng': 31.8516}, 'dropoff': {'lat':  31.0461, 'lng':  31.0461}}
              for c in courses]
    return result


@api.route('/get_options')
def get_options():
    courses = db.get_courses()
    source = Location(lat=float(request.args.get("source_lat")),
                      lng=float(request.args.get("source_lng")))
    destination = Location(lat=float(request.args.get("dest_lat")),
                      lng=float(request.args.get("dest_lng")))

    options = logic_get_options(passenger_source=source,
                                passenger_destination=destination,
                                courses=courses)
    print(options)
    pos = {'lat': float(request.args.get("source_lat")), 'lng':float(request.args.get("source_lng"))}
    print(pos)
    return {'options': options, 'pos': pos}


if __name__ == "__main__":
    api.run()
