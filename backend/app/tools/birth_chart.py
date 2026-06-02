import swisseph as swe
from datetime import datetime
import pytz
from typing import Optional

# Planet names mapping
PLANETS = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MERCURY: "Mercury",
    swe.VENUS: "Venus",
    swe.MARS: "Mars",
    swe.JUPITER: "Jupiter",
    swe.SATURN: "Saturn",
    swe.URANUS: "Uranus",
    swe.NEPTUNE: "Neptune",
    swe.PLUTO: "Pluto",
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

HOUSES = [
    "1st House - Self & Appearance",
    "2nd House - Wealth & Values",
    "3rd House - Communication",
    "4th House - Home & Family",
    "5th House - Creativity & Romance",
    "6th House - Health & Work",
    "7th House - Partnerships",
    "8th House - Transformation",
    "9th House - Philosophy & Travel",
    "10th House - Career & Status",
    "11th House - Friends & Goals",
    "12th House - Spirituality & Hidden"
]

def get_zodiac_sign(longitude: float) -> str:
    sign_index = int(longitude / 30)
    degree = longitude % 30
    return f"{ZODIAC_SIGNS[sign_index]} {degree:.1f}°"

def compute_birth_chart(
    date: str,
    time: str,
    latitude: float,
    longitude: float,
    timezone: str
) -> dict:
    """
    Compute a real birth chart using Swiss Ephemeris.
    Returns planetary positions and house cusps.
    """
    try:
        # Parse date and time
        dt_str = f"{date} {time}"
        
        try:
            dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid date/time format. Use YYYY-MM-DD and HH:MM"
            }
        
        # Validate date range
        if dt_local.year < 1800 or dt_local.year > 2100:
            return {
                "success": False,
                "error": "Birth date must be between 1800 and 2100"
            }
        
        # Convert to UTC
        try:
            tz = pytz.timezone(timezone)
            dt_aware = tz.localize(dt_local)
            dt_utc = dt_aware.astimezone(pytz.UTC)
        except pytz.exceptions.UnknownTimeZoneError:
            dt_utc = dt_local.replace(tzinfo=pytz.UTC)
        
        # Convert to Julian Day Number
        jd = swe.julday(
            dt_utc.year,
            dt_utc.month,
            dt_utc.day,
            dt_utc.hour + dt_utc.minute / 60.0
        )
        
        # Calculate planetary positions
        planets = {}
        for planet_id, planet_name in PLANETS.items():
            try:
                pos, _ = swe.calc_ut(jd, planet_id)
                longitude_deg = pos[0]
                planets[planet_name] = {
                    "longitude": longitude_deg,
                    "sign": get_zodiac_sign(longitude_deg),
                    "retrograde": pos[3] < 0
                }
            except Exception:
                continue
        
        # Calculate house cusps using Placidus system
        try:
            cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
            houses = {}
            for i, cusp in enumerate(cusps):
                houses[HOUSES[i]] = {
                    "longitude": cusp,
                    "sign": get_zodiac_sign(cusp)
                }
            
            ascendant = get_zodiac_sign(ascmc[0])
            midheaven = get_zodiac_sign(ascmc[1])
        except Exception:
            houses = {}
            ascendant = "Unknown"
            midheaven = "Unknown"
        
        return {
            "success": True,
            "birth_details": {
                "date": date,
                "time": time,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone
            },
            "planets": planets,
            "houses": houses,
            "ascendant": ascendant,
            "midheaven": midheaven,
            "chart_summary": f"Ascendant: {ascendant} | Sun: {planets.get('Sun', {}).get('sign', 'Unknown')} | Moon: {planets.get('Moon', {}).get('sign', 'Unknown')}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Chart computation failed: {str(e)}"
        }