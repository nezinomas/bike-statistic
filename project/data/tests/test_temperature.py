import pytest
from datetime import datetime
from ..library.temperature import get_temperature


@pytest.fixture
def mock_weather_api(mocker):
    """Mocks the external API call."""
    return mocker.patch("project.data.library.temperature._fetch_daily_data")


@pytest.fixture
def mock_django_cache(mocker):
    """Mocks Django's cache.get and cache.set."""
    return mocker.patch("project.data.library.temperature.cache")


def test_get_temperature_happy_path(mock_weather_api, mock_django_cache):
    """Scenario: Data is in cache for the exact hour requested."""
    dt = datetime(2026, 2, 6, 14, 0)
    mock_django_cache.get.return_value = {"14": -5.0}

    result = get_temperature(dt)

    assert result == -5.0
    # Should NOT hit the API if data is already in cache
    mock_weather_api.assert_not_called()


def test_get_temperature_fallback_one_hour(mock_weather_api, mock_django_cache):
    """Scenario: 14:00 is missing, API is lagging, fallback to 13:00."""
    dt = datetime(2026, 2, 6, 14, 0)

    # 1. First cache check: 14:00 is missing
    mock_django_cache.get.return_value = {"13": -6.5}
    # 2. API check: Still missing 14:00
    mock_weather_api.return_value = {"12": -7.0, "13": -6.5}

    result = get_temperature(dt)

    # It should return the 13:00 value (-6.5)
    assert result == -6.5
    mock_weather_api.assert_called_once()


def test_get_temperature_zero_degrees_logic(mock_weather_api, mock_django_cache):
    """Scenario: Temperature is exactly 0.0 (Testing our truthiness fix)."""
    dt = datetime(2026, 2, 6, 10, 0)
    mock_django_cache.get.return_value = {"10": 0.0}

    result = get_temperature(dt)

    # Should return 0.0, not move to fallback
    assert result == 0.0


def test_get_temperature_api_and_cache_fail(mock_weather_api, mock_django_cache):
    """Scenario: Neither cache nor API has data for target or fallbacks."""
    dt = datetime(2026, 2, 6, 14, 0)
    mock_django_cache.get.return_value = {}
    mock_weather_api.return_value = None  # API timeout or error

    result = get_temperature(dt)

    assert result is None


def test_get_temperature_force_refresh(mock_weather_api, mock_django_cache):
    """Scenario: Data is in cache, but we force a refresh anyway."""
    dt = datetime(2026, 2, 6, 14, 0)
    mock_django_cache.get.return_value = {"14": -5.0}
    mock_weather_api.return_value = {"14": -4.0}  # New data from API

    result = get_temperature(dt, force_refresh=True)

    assert result == -4.0
    mock_weather_api.assert_called_once()
