from flask import Flask, request

from db import SmileDB, DB_FILENAME, Location, LocationWithName

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
    source = LocationWithName(lat=request.args.get("source_lat"),
                      lng=request.args.get("source_lng"),
                      name=request.args.get("source_name"))
    destination = LocationWithName(lat=request.args.get("dest_lat"),
                      lng=request.args.get("dest_lng"),
                      name=request.args.get("dest_name"))
    print(source, destination)

    options = logic_get_options(passenger_source=source,
                                passenger_destination=destination,
                                courses=courses)
    print(options)
    return options


if __name__ == "__main__":
    api.run(debug=True)
