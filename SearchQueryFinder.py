#final copy, takes 3 parameters, outputs charging station, search query, star, charging station distance
import googlemaps
from googlemaps.exceptions import ApiError

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyAql8j-OIywax4gDUeQ41CHi3ltCzSqabk')

def search_ev_charging_stations(latitude, longitude, radius):
    # Perform a Places API nearby search for EV charging stations
    result = gmaps.places_nearby(location=(latitude, longitude), radius=radius * 1000, keyword='ev charging station')

    # Save the data of each result in a list
    charging_stations = []
    if result['status'] == 'OK' and len(result['results']) > 0:
        for place in result['results']:
            name = place['name']
            address = place['vicinity']
            rating = place.get('rating', 'Not rated')  # Get the rating if available, otherwise set to 'Not rated'
            charging_stations.append({'name': name, 'address': address, 'rating': rating, 'latitude': place['geometry']['location']['lat'], 'longitude': place['geometry']['location']['lng']})
    else:
        print("No EV charging stations found within the specified radius.")

    return charging_stations

def search_nearby_place(charging_station_name, charging_station_address, rating, search_query, charging_station_lat, charging_station_lng, origin_lat, origin_lng):
    try:
        # Perform a Places API search for the search query near the charging station
        result = gmaps.places_nearby(
            location=(charging_station_lat, charging_station_lng),
            radius=300,  # 300 meters
            keyword=search_query
        )

        # Check if any result is found
        if result['status'] == 'OK' and len(result['results']) > 0:
            first_result = result['results'][0]
            # Calculate the distance between the charging station and the origin
            distance_result = gmaps.distance_matrix(origins=(charging_station_lat, charging_station_lng),
                                                     destinations=(origin_lat, origin_lng),
                                                     mode='driving',
                                                     units='metric')
            distance_text = distance_result['rows'][0]['elements'][0]['distance']['text']
            print(f"Charging Station Name: {charging_station_name}")
            print(f"Charging Station Address: {charging_station_address}")
            print(f"Rating: {rating}")
            print(f"Distance from Charging Station to Origin: {distance_text}")
            print(f"Search Query Name: {first_result['name']}")
            print(f"Search Query Address: {first_result['vicinity']}\n")
            return True
        else:
            return False
    except ApiError as e:
        print(f"Error: {e}\n")
        return False

def main():
    # Example current location (latitude and longitude)
    latitude = float(input("Enter current latitude: "))
    longitude = float(input("Enter current longitude: "))

    # Example radius options (A = 3, B = 5, C = 10)
    radius_option = input("Enter radius option (A = 3, B = 5, C = 10): ")
    radius_mapping = {'A': 3, 'B': 5, 'C': 10}
    radius = radius_mapping.get(radius_option.upper())

    if radius is None:
        print("Invalid radius option.")
        return

    # Get the list of EV charging stations
    charging_stations = search_ev_charging_stations(latitude, longitude, radius)

    search_query = input("Enter a search query: ")
    # Search for each company near each EV charging station
    print("\n")
    for station in charging_stations:
        search_nearby_place(station['name'], station['address'], station['rating'], search_query, station['latitude'], station['longitude'], latitude, longitude)

if __name__ == "__main__":
    main()
