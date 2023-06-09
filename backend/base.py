from flask import Flask, request

from logic import dummy_finder, parse_details
from db import SmileDB, DB_FILENAME, Location, LocationWithName

api = Flask(__name__)
db = SmileDB(DB_FILENAME)

DEMO_MODE = True


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

    return options


if __name__ == "__main__":
    api.run(debug=True)
