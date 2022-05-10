import os
import requests

class Request:
    def __init__(self, base_url):
        self._base_url = base_url

    def fetch_data(self, forecast, area):
        url = self._base_url.format(forecast=forecast, area=area)
        resp = requests.get(url)

        if resp.status_code == 404:
            error_msg = "Could not find the are you were looking for."
            raise Exception(error_msg)
        
        return resp.text