import re
from bs4 import BeautifulSoup

from weatherterm.core import ForecastType, Request, Unit, UnitConverter


class WeatherComParser:
    def __init__(self):
        self._forecast = {
            ForecastType.TODAY: self._today_forecast,
            ForecastType.WEEKEND: self._weekend_forecast,
            ForecastType.FIVEDAYS: self._fivedays_forecast,
            ForecastType.TENDAYS: self._tendays_forecast
        }
        self._base_url = 'https://weather.com/weather/{forecast}/l/{area}'
        self._request = Request(self._base_url)
        
        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)
    


    def _today_forecast(self, args):
        raise NotImplementedError() 
    def _weekend_forecast(self, args):
        raise NotImplementedError()
    def _fivedays_forecast(self, args):
        raise NotImplementedError()
    def _tendays_forecast(self, args):
        raise NotImplementedError()

    def run(self, args):
        self._forecast_type = args.forecast_option
        forecast_fn = self._forecast[self._forecast_type]
        return forecast_fn(args)