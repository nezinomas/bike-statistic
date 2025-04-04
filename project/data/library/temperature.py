import requests
from bs4 import BeautifulSoup


class Temperature:
    _url = "https://meteofor.lt/weather-vilnius-4230/now/"

    def __init__(self):
        try:
            self._temperature = self._get_temperature()
        except Exception:  # pylint: disable=broad-except
            self._temperature = None

    @property
    def temperature(self):
        return self._temperature

    def _get_temperature(self):
        page = self._get_weather_page()
        soup = BeautifulSoup(page, "html.parser")

        element = soup.find("temperature-value")

        temperature = element["value"]
        temperature = temperature.replace(",", ".")
        temperature = temperature.replace("−", "-")

        return float(temperature)

    def _get_weather_page(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"  # noqa: E501
            }
            html = requests.get(self._url, headers=headers)
            return html.text

        except Exception:  # pylint: disable=broad-except
            return ""
