#makes text directions for google maps route
import googlemaps
from datetime import datetime

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyAql8j-OIywax4gDUeQ41CHi3ltCzSqabk')

def get_directions(latitude, longitude, destination1, destination2):
    origin = (latitude, longitude)
    
    # Get directions for driving from origin to destination1
    driving_directions = gmaps.directions(origin, destination1, mode="driving")

    # Get directions for walking from destination1 to destination2
    walking_directions = gmaps.directions(destination1, destination2, mode="walking")

    return driving_directions, walking_directions

def main():
    latitude = 45.4270
    longitude = -75.6950
    destination1 = "363 Rideau St, Ottawa, ON"
    destination2 = "275B Laurier Ave E, Ottawa, ON"

    driving_directions, walking_directions = get_directions(latitude, longitude, destination1, destination2)

    print("Driving Directions:")
    for step in driving_directions[0]['legs'][0]['steps']:
        print(step['html_instructions'])

    print("\nWalking Directions:")
    for step in walking_directions[0]['legs'][0]['steps']:
        print(step['html_instructions'])

if __name__ == "__main__":
    main()