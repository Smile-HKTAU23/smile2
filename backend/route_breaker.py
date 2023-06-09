import math
from flask import Flask
from flask_cors import CORS, cross_origin
from math import radians, sin, cos, sqrt, atan2
import googlemaps
import urllib
import folium

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
RADIUS = 10000 #meter
API_KEY = "AIzaSyCxLjTsE3neUN0Z34Sy9DQm0xCSvTjNspU"

gmaps = googlemaps.Client(key=API_KEY)

# TODO: connect to bus stations api
"""
url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=e873e6a2-66c1-494f-a677-f5e77348edb0&limit=5&q=title:jones'  
fileobj = urllib.urlopen(url)
print fileobj.read()
"""
# TODO: connect to google maps api and extract average traffic


@api.route('/options/')
def get_route_coordinates(source, destination):
    # Get the directions
    directions_result = gmaps.directions(source, destination)

    # Extract the polyline points from the result
    route = directions_result[0]['overview_polyline']['points']

    # Decode the polyline points to get the coordinates
    coordinates = decode_polyline(route)

    return coordinates

# Helper function to decode polyline points
def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so loop through
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1F) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            changes[unit] += ~(result >> 1) if result & 1 else (result >> 1)
            coordinates.append(changes[unit] * 1e-5)

    # Convert the coordinates list to a list of tuples
    coordinates = [(coordinates[i], coordinates[i + 1]) for i in range(0, len(coordinates), 2)]

    return coordinates

def get_distance(coor_pass,coor_driver,radius = RADIUS):
    # calculate distance between the points
    # return distance in meters
    lat1,lon1 = coor_pass
    lat2,lon2 = coor_driver
    # Earth's radius in meters
    earth_radius = 6371000

    # Convert coordinates to radians
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate the differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = earth_radius * c

    return distance

def get_route_breakpoints(src_address,dst_address):
    #return driver's route, list of the route coordinates
    return get_route_coordinates(src_address, dst_address)

def order_stations_src_to_dst(route_breakpoints_lst):
    # return tuples of coordinates of bus stations ordered by appearence in the passenger's route
    pass

def get_traffic(coor):
    # return a parameter that represents traffic intensity from excisting data
    pass

def get_average_traffic_stations(stations_lst):
    return [(station,get_traffic(station)) for station in stations_lst]

def sort_average_traffic_stations(stations_traffic_lst):
    return sorted([stations_traffic_lst[i][1] for i in range(len(stations_traffic_lst))])

def calculate_optimal_station(stations_traffic_lst,from_the_end):
    if from_the_end:
        stations_traffic_lst.reverse()

    # optimizing algorithm - temporary naive,
    # idealy neural network trained by data labeled by traffic experts to provide optimal balance between traffic and index priority.
    average_traffic_lst = sort_average_traffic_stations(stations_traffic_lst)
    one_third_index = math.ceil(len(average_traffic_lst) / 3)
    avg_average_traffic = math.fsum(average_traffic_lst) / len(average_traffic_lst)
    for coor,avg_traffic in stations_traffic_lst:
        if avg_traffic > (avg_average_traffic * 2 / 3):
            return coor
    return None
    # return the optimal station that as first as the

def optimal_station(src_name,dst_name,from_the_end=True):
    stations = order_stations_src_to_dst(get_route_breakpoints(src_name,dst_name))
    stations_traffic = get_average_traffic_stations(stations)
    return calculate_optimal_station(stations_traffic,from_the_end)
