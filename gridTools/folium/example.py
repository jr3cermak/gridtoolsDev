import folium
from folium.plugins import Draw

m = folium.Map(location=[-27.23, -48.36], zoom_start=12)

draw = Draw(export=True)

draw.add_to(m)

m
