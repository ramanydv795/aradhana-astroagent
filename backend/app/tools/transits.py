import swisseph as swe
from datetime import datetime
import pytz
from tools.birth_chart import PLANETS, ZODIAC_SIGNS, get_zodiac_sign

def get_daily_transits(
    date: str,
    birth_chart: dict
) -> dict:
    """
    Get current planetary transits and relate them to natal chart.
    """
    try:
        # Parse date
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid date format. Use YYYY-MM-DD"
            }

        # Convert to Julian Day
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)

        # Get current planetary positions
        current_positions = {}
        for planet_id, planet_name in PLANETS.items():
            try:
                pos, _ = swe.calc_ut(jd, planet_id)
                current_positions[planet_name] = {
                    "longitude": pos[0],
                    "sign": get_zodiac_sign(pos[0]),
                    "retrograde": pos[3] < 0
                }
            except Exception:
                continue

        # Compare with natal chart if available
        aspects = []
        if birth_chart and birth_chart.get("success"):
            natal_planets = birth_chart.get("planets", {})
            for transit_planet, transit_data in current_positions.items():
                for natal_planet, natal_data in natal_planets.items():
                    diff = abs(
                        transit_data["longitude"] - natal_data["longitude"]
                    ) % 360
                    if diff > 180:
                        diff = 360 - diff

                    # Check major aspects
                    if diff < 8:
                        aspects.append({
                            "aspect": "Conjunction",
                            "transit_planet": transit_planet,
                            "natal_planet": natal_planet,
                            "orb": round(diff, 2),
                            "meaning": f"{transit_planet} aligns with your natal {natal_planet} — powerful activation"
                        })
                    elif abs(diff - 60) < 6:
                        aspects.append({
                            "aspect": "Sextile",
                            "transit_planet": transit_planet,
                            "natal_planet": natal_planet,
                            "orb": round(abs(diff - 60), 2),
                            "meaning": f"{transit_planet} sextiles your natal {natal_planet} — harmonious opportunity"
                        })
                    elif abs(diff - 90) < 8:
                        aspects.append({
                            "aspect": "Square",
                            "transit_planet": transit_planet,
                            "natal_planet": natal_planet,
                            "orb": round(abs(diff - 90), 2),
                            "meaning": f"{transit_planet} squares your natal {natal_planet} — tension and growth"
                        })
                    elif abs(diff - 120) < 8:
                        aspects.append({
                            "aspect": "Trine",
                            "transit_planet": transit_planet,
                            "natal_planet": natal_planet,
                            "orb": round(abs(diff - 120), 2),
                            "meaning": f"{transit_planet} trines your natal {natal_planet} — flowing energy"
                        })
                    elif abs(diff - 180) < 8:
                        aspects.append({
                            "aspect": "Opposition",
                            "transit_planet": transit_planet,
                            "natal_planet": natal_planet,
                            "orb": round(abs(diff - 180), 2),
                            "meaning": f"{transit_planet} opposes your natal {natal_planet} — balance needed"
                        })

        return {
            "success": True,
            "date": date,
            "current_positions": current_positions,
            "aspects_to_natal": aspects[:10],  # Top 10 most relevant
            "summary": f"Today {len(aspects)} planetary aspects are active in your chart"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Transit calculation failed: {str(e)}"
        }