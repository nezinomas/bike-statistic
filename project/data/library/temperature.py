import json
import urllib.request
from datetime import datetime

from django.core.cache import cache

BASE_URL = "https://api.meteo.lt/v1/stations/vilniaus-ams/observations"


def get_temperature(dt: datetime, force_refresh: bool = False) -> float | None:
    """
    Retrieves the temperature for a specific hour using a flattened logic flow.
    """
    date_str = dt.strftime("%Y-%m-%d")
    hour_key = str(dt.hour).zfill(2)
    cache_key = f"weather_{date_str}"

    cached_data = cache.get(cache_key) or {}

    # 2. Determine if we need to fetch
    has_target_hour = hour_key in cached_data
    if not force_refresh and has_target_hour:
        return cached_data.get(hour_key)

    # 3. Fetch from API
    new_data = _fetch_daily_data(date_str)
    if not new_data:
        # If API fails, return what we had in cache (even if hour is missing)
        return cached_data.get(hour_key)

    # 4. Merge and Update Cache
    updated_data = cached_data | new_data
    cache.set(cache_key, updated_data)

    return updated_data.get(hour_key)


def _fetch_daily_data(date_str: str) -> dict | None:
    """Internal helper to fetch and parse the external API."""
    url = f"{BASE_URL}/{date_str}"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status != 200:
                return None

            raw = json.loads(response.read().decode())
            # Convert large observation list into a lean {hour: temp} dictionary
            return {
                obs["observationTimeUtc"][11:13]: obs.get("airTemperature")
                for obs in raw.get("observations", [])
                if obs.get("observationTimeUtc", "").startswith(date_str)
            }
    except Exception as e:
        return None
