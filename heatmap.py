import requests
from bs4 import BeautifulSoup
import geoip2.database
import json
import folium
from folium.plugins import HeatMap
import os

# Define the URLs for the 5 txt lists of IP addresses and their corresponding output file names
url_pairs = [
    ('https://raw.githubusercontent.com/CTH-JC-CC/APT28-IOC/main/Additional-IPS.txt', 'Additional-IPS.json'),
    ('https://raw.githubusercontent.com/CTH-JC-CC/APT28-IOC/main/Amber-1-IOC-IP.txt', 'Amber-1-IOC-IP.json'),
    ('https://raw.githubusercontent.com/CTH-JC-CC/APT28-IOC/main/Amber-2-IOC-IP.txt', 'Amber-2-IOC-IP.json'),
    ('https://raw.githubusercontent.com/CTH-JC-CC/APT28-IOC/main/Grey-IOC-IP.txt', 'Grey-IOC-IP.json'),
    ('https://raw.githubusercontent.com/CTH-JC-CC/APT28-IOC/main/Red-IOC.txt', 'Red-IOC.json')
]

# Load the GeoIP2 database
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

# Geolocate each IP address using the GeoIP2 API and write to output files
for url, out_filename in url_pairs:
    response = requests.get(url)
    ip_addresses = response.text.splitlines()

    # Create dictionaries to store the geolocation data and the IPs with missing data
    geolocation_data = {}
    missing_ips = []

    for ip in ip_addresses:
        try:
            response = reader.city(ip)
            latitude = response.location.latitude
            longitude = response.location.longitude
            if latitude is None or longitude is None or latitude == 0 or longitude == 0:
                continue
            geolocation_data[ip] = (latitude, longitude)
        except:
            missing_ips.append(ip)

    with open(out_filename, 'w') as f:
        json.dump(geolocation_data, f)

    # Create a Folium map and add a heatmap layer based on the geolocation data
    m = folium.Map(location=[30, 0], zoom_start=2)
    heatmap_layer = folium.FeatureGroup(name='Heatmap')
    heatmap_layer.add_child(folium.plugins.HeatMap(list(geolocation_data.values()), min_opacity=0.2))
    m.add_child(heatmap_layer)
    folium.LayerControl().add_to(m)
    m.save(f'{out_filename}.html')

    # Write the missing IPs to a separate file
    missing_ips_file = f'{out_filename}_missing_ips.txt'
    if missing_ips:
        with open(missing_ips_file, 'w') as f:
            f.write('\n'.join(missing_ips))

# Combine the geolocation data from all the files into one dictionary and write to output file
combined_data = {}
missing_ips = []
for _, out_filename in url_pairs:
    try:
        with open(out_filename, 'r') as f:
            data = json.load(f)
            combined_data.update(data)

        missing_ips_file = f'{out_filename}_missing_ips.txt'
        if os.path.exists(missing_ips_file):
            with open(missing_ips_file, 'r') as f:
                missing_ips.extend(f.read().splitlines())

    except FileNotFoundError:
        print(f'Skipping {out_filename} - no geolocation data found')
combined_data_filtered = {k: v for k, v in combined_data.items() if v is not None and v != (0, 0)}

with open('APT28_overview.json', 'w') as f:
    json.dump(combined_data_filtered, f)

# Create a Folium map and add a heatmap layer based on the combined geolocation data
m = folium.Map(location=[30, 0], zoom_start=2)
heatmap_layer = folium.FeatureGroup(name='Heatmap')
heatmap_layer.add_child(folium.plugins.HeatMap(list(combined_data_filtered.values()), min_opacity=0.2))
m.add_child(heatmap_layer)
folium.LayerControl().add_to(m)
m.save('APT28_overview.html')

