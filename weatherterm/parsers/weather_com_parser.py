import re
from bs4 import BeautifulSoup
from datetime import date

from weatherterm.core import ForecastType, Request, Unit, UnitConverter
from weatherterm.core.forecast import Forecast


class WeatherComParser:
    def __init__(self):
        self._forecast = {
            ForecastType.TODAY: self._today_forecast,
            ForecastType.WEEKEND: self._weekend_forecast,
            ForecastType.FIVEDAYS: self._fivedays_forecast,
            ForecastType.TENDAYS: self._tendays_forecast
        }
        self._base_url = 'https://weather.com/weather/{forecast}/l/{area}?unit=e'
        self._request = Request(self._base_url)
        self._only_digits_regex = re.compile('[0-9]+')
        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)

    def _clear_str_number(self, str_number):
        result = self._only_digits_regex.match(str_number)
        return '--' if result is None else result.group()
    
    def _fix_details(self, str_details):
        str_details['Wind'] = re.sub('Wind Direction', '', str_details['Wind'])
        str_details['Pressure'] = re.sub('Arrow *(Up)|(Down)', '', str_details['Pressure'])

        return str_details        

    def future_forecast_parser(self, area_code, n_days):
        content = self._request.fetch_data('tenday', area_code)
        bs = BeautifulSoup(content, 'html.parser')

        location_span_regex = re.compile('LocationPageTitle--LocationText*')
        location = bs.find('span', {'class': location_span_regex}).text

        timestamp_div_regex = re.compile('DailyForecast--timestamp*')
        timestamp = bs.find('div', {'class': timestamp_div_regex}).text

        list_divs_regex = re.compile('DailyForecast--DisclosureList*')
        list_divs_forecasts = bs.find('div', {'class': list_divs_regex})

        forecast_details = list_divs_forecasts.find_all('details')[:n_days]

        forecast_results = []
        for curr_forecast in forecast_details:
            summ_regex = re.compile('DetailsSummary--DetailsSummary*')
            hilo_temp_regex = re.compile('DetailsSummary--temperature*')
            condition_regex = re.compile('DetailsSummary--extendedData*')
            precip_regex = re.compile('DetailsSummary--precip*')
            wind_regex = re.compile('Wind--windWrapper*')

            summary = curr_forecast.find('div', {'class': summ_regex})

            curr_day = summary.find('h3').text
            hilo_temps = summary.find('div', {'class': hilo_temp_regex}).text
            condition = summary.find('span', {'class': condition_regex}).text
            rain_chance = summary.find('div', {'class': precip_regex}).span.text
            wind = summary.find('span', {'class': wind_regex}).text

            hi, lo = [self._clear_str_number(temp) for temp in hilo_temps.split('/')]

            forecast_results.append(
                Forecast(
                location=location,
                timestamp=timestamp,
                wind=wind,
                high_temp=hi,
                low_temp=lo,
                desc=condition,
                forecast_date=curr_day,
                rain_chance=rain_chance,
                forecast_type=ForecastType.TENDAYS
                )
            )

        return forecast_results

    def _today_forecast(self, args):
        content = self._request.fetch_data(args.forecast_option.value, args.area_code)
        bs = BeautifulSoup(content, 'html.parser')

        location_header_regex = re.compile('CurrentConditions--location*')
        location = bs.find('h1', {'class': location_header_regex}).text

        timestamp_span_regex = re.compile('CurrentConditions--timestamp*')
        timestamp = bs.find('span', {'class': timestamp_span_regex}).text
        
        primary_div_regex = re.compile('CurrentConditions--primary*')
        temp_span_regex = re.compile('CurrentConditions--tempValue*')
        phrase_div_regex = re.compile('CurrentConditions--phraseValue*')

        container = bs.find('div', {'class': primary_div_regex})
        curr_temp = container.find('span', {'class': temp_span_regex}).text
        description = container.find('div', {'class': phrase_div_regex}).text

        feelsLike_temp_div_regex = re.compile('TodayDetailsCard--feelsLikeTemp*')
        sunrise_settime_p_regex = re.compile('SunriseSunset--dateValue*')
        addn_details_div_regex = re.compile('TodayDetailsCard--detailsContainer*')

        details_container = bs.find('div', {'id': 'todayDetails'}).section
        

        feelsLikeTemp = details_container.find('div', {'class': feelsLike_temp_div_regex}).text
        feelsLikeTemp = re.sub('[a-zA-Z ]', '', feelsLikeTemp)

        sunrise_sunset_times = details_container.find_all('p', {'class': sunrise_settime_p_regex})

        sunrise_time = sunrise_sunset_times[0].text
        sunset_time = sunrise_sunset_times[1].text

        addn_details_cont = details_container.find('div', {'class': addn_details_div_regex}).children

        addn_details = {}
        for listItem in addn_details_cont:
            details = listItem.find_all('div')
            detailTitle = details[0].text
            detailBody = details[1].text

            addn_details[detailTitle] = detailBody

        addn_details = self._fix_details(addn_details)        

        hi, lo = [self._clear_str_number(temp) for temp in addn_details['High / Low'].split('/')]

        td_forecast = Forecast(
            location,
            timestamp,
            self._clear_str_number(curr_temp),
            addn_details['Wind'],
            addn_details['Humidity'],
            hi,
            lo,
            description,
            feels_like=feelsLikeTemp,
            dew_point=addn_details['Dew Point'],
            pressure=addn_details['Pressure'],
            uv_index=addn_details['UV Index'],
            visibility=addn_details['Visibility'],
            moon_phase=addn_details['Moon Phase'],
            sunrise=sunrise_time,
            sunset=sunset_time
        )

        return [td_forecast]

    def _weekend_forecast(self, args):
        raise NotImplementedError()

    def _fivedays_forecast(self, args):
        return self.future_forecast_parser(args.area_code, n_days=5)

    def _tendays_forecast(self, args):
        return self.future_forecast_parser(args.area_code, n_days=10)

    def run(self, args):
        self._forecast_type = args.forecast_option
        forecast_fn = self._forecast[self._forecast_type]
        return forecast_fn(args)