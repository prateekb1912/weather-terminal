import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Request:
    def __init__(self, base_url):
        self._phantomjs_path = os.path.join(os.curdir, 'phantomjs/bin/phantomjs')
        self._base_url = base_url

        options = Options()
        options.add_argument('-profile')
        options.add_argument('/home/marvin/snap/firefox/common/.mozilla/firefox')
        self._driver = webdriver.Firefox(options=options)
    
    def fetch_data(self, forecast, area):
        url = self._base_url.format(forecast=forecast, area=area)
        self._driver.get(url)

        if self._driver.title == '404 Not Found':
            error_msg = "Could not find the are you were looking for."
            raise Exception(error_msg)
        
        return self._driver.page_source
