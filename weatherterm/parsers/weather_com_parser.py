import re

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

        self._temp_regex = re.compile('([0-9]+)\D{,2}')
        self._only_digits_regex = re.compile('[0-9]+')
        
        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)
    
    def _get_data(self, container, search_items):
        scraped_data = {}

        for k,v in search_items.items():
            res = container.find(v, class_ = k)
            data = None if res is None else res.get_text()

            if data is not None:
                scraped_data[k] = data
        
        return scraped_data

    def _parse(self, container, criteria):
        results = [self._get_data(item, criteria) for item in container.children]

        return [res for res in results if res]

    def _clear_str_number(self, str_number):
        res = self._only_digits_regex.match(str_number)

        return '--' if res is None else res.group()

    def _get_additional_info(self, content):
        data = tuple(item.td.span.get_text() for item in content.table.tbody.children)

        return data[:2]


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