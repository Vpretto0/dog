import geocoder
import socket
 
def get_coordinates():
    try:
        location = geocoder.ip('me')
        latitude, longitude = location.latlng
        return latitude, longitude
    except Exception as e:
        print(f"Error retrieving coordinates: {e}")
        return None
    
def main():
    coordinates = get_coordinates()
    if coordinates:
        latitude, longitude = coordinates
        print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
    else:
        print("Could not retrieve coordinates.")
        
if __name__ == "__main__":
    main()
