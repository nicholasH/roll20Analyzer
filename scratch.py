import os
import re
import time

import sys
from telnetlib import EC

from aiohttp.hdrs import PRAGMA
from bs4 import BeautifulSoup
from kivy.uix.widget import Widget
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
import sqlite3
from datetime import datetime, date,timedelta
import pickle
import kivy

from selenium.webdriver.support.wait import WebDriverWait

import  DBhandler



import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label


class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()