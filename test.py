import folium
from folium.plugins import HeatMap

import matplotlib.pyplot as plt
from pyproj import Transformer

# define the ArcGIS object
arcgis_obj = {'rings': [[[-8416053.9734, 5644829.9895], [-8415830.4228, 5644967.4077], [-8415745.6855, 5645019.4943], [-8415606.5284, 5644791.8503], [-8415794.2594, 5644677.7493], [-8416052.7906, 5644520.6078], [-8416151.3765, 5644770.1128], [-8416053.9734, 5644829.9895]]], 'spatialReference': {'wkid': 102100, 'latestWkid': 3857}}

# convert the coordinates to latitude and longitude
lon_lat = []
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")

for x, y in arcgis_obj['rings'][0]:
    lon_lat.append(list(transformer.transform(x, y)))

print(lon_lat)

# create a folium map centered on the polygon
map_center = [sum(lon for lon, lat in lon_lat)/len(lon_lat), sum(lat for lon, lat in lon_lat)/len(lon_lat)]
m = folium.Map(location=map_center, zoom_start=13)

print(map_center)

# add the polygon to the map
folium.Polygon(locations=lon_lat, color='blue', fill=True, fill_color='blue').add_to(m)

# display the map
m.save("data/map.html")