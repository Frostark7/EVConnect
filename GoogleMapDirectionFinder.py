#ask for the 3 parameters, prints out the name and address of each charging station that obey the parameters

import googlemaps
from googlemaps.exceptions import ApiError

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyAql8j-OIywax4gDUeQ41CHi3ltCzSqabk')

def search_ev_charging_stations(latitude, longitude, radius):
    # Perform a Places API nearby search for EV charging stations
    result = gmaps.places_nearby(location=(latitude, longitude), radius=radius * 1000, keyword='Electric vehicle charging station')

    # Save the data of each result in a list
    charging_stations = []
    if result['status'] == 'OK' and len(result['results']) > 0:
        for place in result['results']:
            name = place['name']
            address = place['vicinity']
            charging_stations.append({'name': name, 'address': address})
    else:
        print("No EV charging stations found within the specified radius.")

    return charging_stations

def search_nearby_place(company_name, company_address, search_query):
    try:
        # Geocode the company address to get its latitude and longitude
        geocode_result = gmaps.geocode(company_address)
        if geocode_result and len(geocode_result) > 0:
            company_location = geocode_result[0]['geometry']['location']

            # Perform a Places API nearby search for the search query near the company location
            result = gmaps.places_nearby(
                location=(company_location['lat'], company_location['lng']),
                radius=150,  # 150 meters
                keyword=search_query
            )

            # Check if any result is within 150m of the company location
            if result['status'] == 'OK' and len(result['results']) > 0:
                print(f"Company Name: {company_name}")
                print(f"Company Address: {company_address}\n")
                return True
            else:
                return False
        else:
            print(f"Failed to geocode address for '{company_name}' at '{company_address}'\n")
            return False
    except ApiError as e:
        print(f"Error: {e}\n")
        return False
    # Implement search_nearby_place function from Test2 here

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
        search_nearby_place(station['name'], station['address'], search_query)

if __name__ == "__main__":
    main()