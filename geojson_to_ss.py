import requests
from urllib.parse import quote

# Your Mapbox access token
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoienlqeTExOCIsImEiOiJjbG9vNDhhem8yeDBtMmlxcDJlZXM0cDFsIn0.50treFn722VMWsjEsCCpPw'

# Function to geocode an address
def geocode_address(address):
    geocode_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote(address)}.json?access_token={MAPBOX_ACCESS_TOKEN}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        json = response.json()
        # Assuming you want the first result
        coordinates = json['features'][0]['center']
        return coordinates
    else:
        raise Exception(f"Geocoding API error: {response.status_code}")

# Function to get static image from Mapbox
def get_static_map_image(lon, lat, username='zyjy118', style_id='clogyeist005901nzfv9veyfa', zoom=16, width=300, height=200):
    static_image_url = f"https://api.mapbox.com/styles/v1/{username}/{style_id}/static/{lon},{lat},{zoom}/{width}x{height}@2x?access_token=YOUR_MAPBOX_ACCESS_TOKEN"
    response = requests.get(static_image_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Static Images API error: {response.status_code}")

# Main process
def main():
    # Load addresses from a file
    with open('addresses.txt', 'r') as file:
        addresses = file.readlines()

    # Process each address
    for address in addresses:
        address = address.strip()
        try:
            # Geocode the address
            lon, lat = geocode_address(address)
            
            # Get the static map image
            image_data = get_static_map_image(lon, lat)
            
            # Save the image
            with open(f"{address.replace(' ', '_')}.png", 'wb') as img_file:
                img_file.write(image_data)
            print(f"Image saved for address: {address}")
        
        except Exception as e:
            print(f"Failed to process address {address}: {e}")

# Run the script
if __name__ == "__main__":
    main()
