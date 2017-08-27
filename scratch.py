import contextlib
import os

import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import sys

from selenium.common.exceptions import TimeoutException

URL = 'https://app.roll20.net/sessions/new'
chromeDriver = os.path.join(sys.path[0], "chromedriver.exe")
browser = webdriver.Chrome(chromeDriver)
browser.get(URL)
wait = ui.WebDriverWait(browser, 120) # timeout after 10 seconds

try:
    results = wait.until(lambda driver: driver.find_elements_by_class_name('loggedin'))

    if len(results) > 0:
        print("continue")
    else:
        print("error website changes")
except TimeoutException:
    browser.close()
    print("error timeout")
