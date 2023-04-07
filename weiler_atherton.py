# import shapely
import folium
from arcgis.geometry import Polygon

OTTAWA = [45.4215, -75.6972]

def create_test_map(features):
    coords_1 = [
          [
            [
              -75.67968677643513,
              45.41560770492214
            ],
            [
              -75.67968677643513,
              45.423823130398006
            ],
            [
              -75.69377985257785,
              45.423823130398006
            ],
            [
              -75.69377985257785,
              45.41560770492214
            ],
            [
              -75.67968677643513,
              45.41560770492214
            ]
          ]
        ]
    coords_2 = [
          [
            [
              -75.6927447678894,
              45.42650545942101
            ],
            [
              -75.68709161305293,
              45.41991117211023
            ],
            [
              -75.6804829954265,
              45.4264495788662
            ],
            [
              -75.6927447678894,
              45.42650545942101
            ]
          ]
        ]

    m = folium.Map(location=OTTAWA, zoom_start=13)
    Polygon({"rings" : [coords_1], "spatialReference" : {"wkid" : 4326}}).add_to(m) # rectangle
    Polygon({"rings" : [coords_2], "spatialReference" : {"wkid" : 4326}}).add_to(m) # triangle 
    m.save("data/map-weiler-atherton.html")
    


