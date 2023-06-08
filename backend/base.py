from flask import Flask, request

from db import SmileDB, DB_FILENAME, Location

api = Flask(__name__)
db = SmileDB(DB_FILENAME)


def logic_get_options(passenger_source: Location,
                      passenger_destination: Location,
                      courses):
    print("logic_get_options() is a mock - returning first courses...")
    result = [{"id": c.id, 'pickup': {'lat': 33.0461, 'lng': 34.8516}, 'dropoff': {'lat':  34.0461, 'lng':  33.0461}}
              for c in courses]
    return result


@api.route('/get_options')
def get_options():
    courses = db.get_courses()
    source = Location(lat=request.args.get("source_lat"),
                      lng=request.args.get("source_lng"))
    destination = Location(lat=request.args.get("dest_lat"),
                      lng=request.args.get("dest_lng"))

    options = logic_get_options(passenger_source=source,
                                passenger_destination=destination,
                                courses=courses)
    print(options)
    return options


if __name__ == "__main__":
    api.run()
