import dateTime as dateTime
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
import threading
import time
import DBhandler

def getdate():
    message = DBhandler.getMessageDateTime(dateTime(2017,7,10))
    