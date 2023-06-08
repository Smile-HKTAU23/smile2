from flask import Flask
from flask_cors import CORS, cross_origin

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'


@api.route('/options/')
def api_get_options():    
    result = get_options(request.body)
    return result

def get_options(details):


    return [{'id': '111111', 'pickup': {'lat': 33.0461, 'lng': 34.8516}, 'dropoff': {'lat': 34.0461, 'lng': 34.8516} }, 
            {'id': '222222', 'pickup': {'lat': 33.0461, 'lng': 34.8516}, 'dropoff': {'lat': 35.0461, 'lng': 34.8516} }]


def main():
    details = {
    'passenger':
        {'source': {'lat': 33.0461, 'lng': 34.8516},
        'destination': {'lat': 34.0461, 'lng': 34.8516}},
    'courses':
        [
            {'id': '111111',
            'source': {'lat': 33.0461, 'lng': 34.8516},
            'destination': {'lat': 34.0461, 'lng': 34.8516}},
            {'id': '222222',
            'source': {'lat': 33.0461, 'lng': 34.8516},
            'destination': {'lat': 34.0461, 'lng': 34.8516}},
        ],
        # 'points_of_interest': [{'lat': 0, 'lon': 0}, {'lat': 0, 'lon': 0}, {'lat': 0, 'lon': 0}]
    }
    result = get_options(details)
    print(result)
    


if __name__ == "__main__":
    main()