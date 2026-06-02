from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from timezonefinder import TimezoneFinder
import json

def geocode_place(place: str) -> dict:
    """
    Resolve a place name to latitude, longitude, and timezone.
    Required for accurate birth chart calculations.
    """
    try:
        geolocator = Nominatim(user_agent="aradhana-astroagent")
        location = geolocator.geocode(place, timeout=10)
        
        if not location:
            return {
                "success": False,
                "error": f"Could not find location: {place}"
            }
        
        # Get timezone for coordinates
        tf = TimezoneFinder()
        timezone = tf.timezone_at(
            lat=location.latitude,
            lng=location.longitude
        )
        
        return {
            "success": True,
            "place": place,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": timezone or "UTC",
            "full_address": location.address
        }
        
    except GeocoderTimedOut:
        return {
            "success": False,
            "error": "Geocoding service timed out. Please try again."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }