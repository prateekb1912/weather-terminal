from datetime import date

from .forecast_type import ForecastType

class Forecast:
    def __init__(self, current_temp, wind, humidity=None,
    high_temp=None, low_temp=None, desc='', forecast_date=None, feels_like=None, 
    sunrise=None, sunset=None, moonrise=None, moonset=None,
    rain_chance=None, rain_amt=None,
    forecast_type=ForecastType.TODAY):
        self._current_temp = current_temp
        self._high_temp = high_temp
        self._low_temp = low_temp
        self._humidity = humidity
        self._description = desc
        self._wind = wind
        self._feels_like = feels_like
        self._sunrise = sunrise
        self._sunset = sunset
        self._moonrise = moonrise
        self._moonset = moonset
        self._rain_chance = rain_chance
        self.rain_amount = rain_amt
        self._forecast_type = forecast_type

        if forecast_date is None:
            self._forecast_date = date.today()
        else:
            self._forecast_date = forecast_date
    
    @property
    def forecast_date(self):
        return self._forecast_date
    
    @forecast_date.setter
    def forecast_date(self, forecast_date):
        self._forecast_date = forecast_date.strftime("%a %b %d")
    
    @property
    def current_temp(self):
        return self._current_temp
    
    @property
    def humidity(self):
        return self._humidity
    
    @property
    def wind(self):
        return self._wind
    
    @property
    def description(self):
        return self._description

    def __str__(self):
        temperature = None
        offset = ' '*10

        if self._forecast_type == ForecastType.TODAY:
            temperature = (
                f'{offset}{self.current_temp}\xb0 ({self.description})\n'
                f'{offset}High {self._high_temp}\xb0 / '
                f'Low {self._low_temp}\xb0 '
            )
        else:
            temperature = (
                f'{offset}High {self._high_temp}\xb0 / '
                f'Low {self._low_temp}\xb0 '
            )
        
        return (
                f'>> {self.forecast_date}\n'
                f'{temperature}\n'
                f'{offset}Wind: {self._wind} / Humidity: {self._humidity}\n'
            )
