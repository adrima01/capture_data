import requests

ip = input("Enter IP Address: ")
url = 'https://ip.circl.lu/geolookup/' + ip

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
    if "Latitude (average)" in data[1]["country_info"]:
        lat = data[1]["country_info"]["Latitude (average)"]
    else:
        lat = -1000
    if "Longitude (average)" in data[1]["country_info"]:
        long = data[1]["country_info"]["Longitude (average)"]
    else:
        long = -1000
    print(lat, long)
else:
    print(f"Error: {response.status_code}")