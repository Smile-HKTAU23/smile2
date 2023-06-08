from flask import Flask
from flask_cors import CORS, cross_origin
from math import radians, sin, cos, sqrt, atan2
import googlemaps
import folium

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
RADIUS = 750 #meter
API_KEY = "AIzaSyCxLjTsE3neUN0Z34Sy9DQm0xCSvTjNspU"

gmaps = googlemaps.Client(key=API_KEY)

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

def get_driver_route(src_address,dst_address):
    #return driver's route, list of the route coordinates
    return get_route_coordinates(src_address, dst_address)

def unite_coor(lat,lon):
    return lat,lon



def get_drivers_near_coordinate(drivers_route_dict,coor,radius=RADIUS):
    filtered_dict = {}
    min_distance_dict = {}
    for driver_id, coordinates in drivers_route_dict.items():
        min_distance = float('inf')
        nearest_coordinate = None
        for coordinate in coordinates:
            distance = get_distance(coordinate, coor)
            if distance <= radius and distance < min_distance:
                min_distance = distance
                nearest_coordinate = coordinate
        if nearest_coordinate is not None:
            filtered_dict[driver_id] = coordinates
            min_distance_dict[driver_id] = nearest_coordinate
    return filtered_dict, min_distance_dict

#---- what is the diff between the last 2
def get_drivers_near_dst(drivers_route_dict,dst_coor,radius=RADIUS):
    drivers_near_dst, drivers_dropoff = get_drivers_near_coordinate(drivers_route_dict, dst_coor, radius)
    sorted_items = sorted(drivers_dropoff.items(), key=lambda item: get_distance(item[1], dst_coor))
    return sorted_items, drivers_dropoff

def get_rides(drivers_route_dict,src_coor,dst_coor,radius=RADIUS):
    drivers_near_src,pickup_dict = get_drivers_near_coordinate(drivers_route_dict,src_coor,radius)
    matching_drivers,dropoff_dict = get_drivers_near_dst(drivers_route_dict,dst_coor,radius)
    maximum = min(3,len(matching_drivers))
    return [{'id':matching_drivers[i][0],'pickup':{'lat':pickup_dict[matching_drivers[i][0]][0],'lon':pickup_dict[matching_drivers[i][0]][1]},'dropoff':{'lat':dropoff_dict[matching_drivers[i][0]][0],'lon':dropoff_dict[matching_drivers[i][0]][1]}} for i in range(maximum)]
    #return 0-3 best rides

def api_get_options():
    result = get_options(request.body)
    return result

def get_options(details):
    #return 0-3 options for rides
    #return object = {'id': '111111', 'pickup': {'lat': 0, 'lon': 0}, 'dropoff': {'lat': 0, 'lon': 0} }

    return [{'id': '111111', 'pickup': {'lat': 0, 'lon': 0}, 'dropoff': {'lat': 0, 'lon': 0} }, 
            {'id': '222222', 'pickup': {'lat': 0, 'lon': 0}, 'dropoff': {'lat': 0, 'lon': 0} }]

def test1(coordinates):


    # Set the initial map location
    map_center = [0, 0]
    zoom_level = 2

    # Create a map object
    m = folium.Map(location=map_center, zoom_start=zoom_level)

    def add_coordinates_to_map(coordinates):
        # Add markers for each coordinate
        for coord in coordinates:
            folium.Marker(coord).add_to(m)

    # Add coordinates to the map
    add_coordinates_to_map(coordinates)

    # Save the map to an HTML file
    m.save('map.html')

def main():
    details = {
    'passenger':
        {'source': {'lat': 0, 'lon': 0},
        'destination': {'lat': 0, 'lon': 0}},
    'courses':
        [
            {'id': '111111',
            'source': {'lat': 0, 'lon': 0},
            'destination': {'lat': 0, 'lon': 0}},
            {'id': '222222',
            'source': {'lat': 0, 'lon': 0},
            'destination': {'lat': 0, 'lon': 0}},
        ],
        # 'points_of_interest': [{'lat': 0, 'lon': 0}, {'lat': 0, 'lon': 0}, {'lat': 0, 'lon': 0}]

    }
    #-----not relevant:
    source_location = 'Shlomzion Ramat Gan'
    destination_location = 'Tel Aviv University'

    route_coordinates = get_route_coordinates(source_location, destination_location)
    test1(route_coordinates)

    # Print the coordinates
    print(route_coordinates)
    #-------

    result = get_options(details)
    print(result)
    


if __name__ == "__main__":
    main()