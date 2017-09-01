from random import randint

import re

from datetime import datetime

from kivy import Config
from kivy.app import App
from kivy.base import EventLoop
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix import popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

import analyze
Config.set('input', 'mouse', 'mouse,disable_multitouch')


class genDateInput(TextInput):
    multiline = False
    input_filter = StringProperty("int")
    chars = NumericProperty(4)

    def insert_text(self, substring, from_undo=False):
        substring = substring[:self.chars - len(self.text)]
        return super(genDateInput, self).insert_text(substring, from_undo=from_undo)

    def on_disabled(self, instance, value):
        if value:
            self.opacity = 0
        else:
            self.opacity = 1
        return super(genDateInput, self)


class RightClickTextInput(TextInput):

    def on_touch_down(self, touch):

        super(RightClickTextInput,self).on_touch_down(touch)

        if touch.button == 'right':
            print("right mouse clicked")
            pos = super(RightClickTextInput,self).to_local(*self._long_touch_pos, relative=True)

            self._show_cut_copy_paste(
                pos, EventLoop.window, mode='copy')

class dndUI(BoxLayout):
    text = "Hello world"
    def run(self,textbox):
        textbox.text = analyze.analyze()


    def runToday(self,textbox):
        textbox.text =analyze.analyzeToday()

    def runByDate(self,outputText, day, month, year, day1, month1, year1, active):
        popup = Popup(title='Date Error',
                      content=Label(text='invalid date'),
                      size_hint=(None, None), size=(400, 200))

        try:
            date0 = datetime(int(year), int(month), int(day))
        except ValueError:

            popup.open()
            return

        if active:
            try:
                date1 = datetime(int(year1), int(month1), int(day1))
            except ValueError:
                popup.open()
                return
            if date1 < date0:
                popup.open()
                return
            outputText.text = analyze.analyzeDateRange(date0, date1)
        else:
            outputText.text = analyze.analyzeDate(date0)






class dndUIApp(App):
    def build(self):
        return dndUI()


if __name__ == '__main__':
    dndUIApp().run()
