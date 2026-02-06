import json
import urllib.request
from datetime import datetime, timedelta

from django.core.cache import cache

BASE_URL = "https://api.meteo.lt/v1/stations/vilniaus-ams/observations"


def get_temperature(dt: datetime, force_refresh: bool = False) -> float | None:
    """
    Retrieves the temperature for a specific hour using a flattened logic flow.
    """
    date_str = dt.strftime("%Y-%m-%d")
    cache_key = f"weather_{date_str}"

    # 1. Pull data from cache
    cached_data = cache.get(cache_key) or {}
    target_hour_str = str(dt.hour).zfill(2)

    # 2. Fetch from API if target is missing or refresh is forced
    if force_refresh or target_hour_str not in cached_data:
        if new_data := _fetch_daily_data(date_str):
            cached_data = cached_data | new_data
            cache.set(cache_key, cached_data)

    # 3. Fallback Loop: 0h -> -1h -> -2h
    for offset in [0, 1, 2]:
        check_time = dt - timedelta(hours=offset)

        # Guard: Stay within the same calendar day for simplicity
        if check_time.date() != dt.date():
            continue

        hour_key = str(check_time.hour).zfill(2)

        # CORRECTED: Actually return the value if it exists!
        if hour_key in cached_data:
            return cached_data[hour_key]

    return None


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
