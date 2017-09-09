from flask import Flask, render_template
import json

app = Flask(__name__)


parkname_to_address = {}


def get_lat_long(park):
    try:
        park_address = parkname_to_address[park]
        nominatim_encoder = Nominatim()
        location = nominatim_encoder.geocode(park_address)
    except:
        google_api_key = pickle.load(open("google_geocoder_api.creds","rb"))
        google_encoder = GoogleV3(google_api_key)
        park_address = park + ", nyc"
        location = google_encoder.geocode(park_address)
    if location:
        return location.latitude, location.longitude
    else:
        return "no address information", "no address information"


def to_geojson(coordinates):
    dicter = {}
    dicter["type"] = "Feature"
    dicter["properties"] = {}
    dicter["geometry"] = {
        "type":"Point",
        "coordinates":[float(coordinates[0]), float(coordinates[1])]
        }
    return dicter

@app.route("/map_visual",methods=["GET","POST"])
def map_visual():
    locations = get_locations()
    locations = [to_geojson(location) for location in locations]
    return render_template("map_visual.html",locations=json.dumps(locations))
