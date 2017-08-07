from random import randint

from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector



def callback(instance):
    print('The button <%s> is being pressed' % instance.text)

btn1 = Button(text='Hello world 1')
btn1.bind(on_press=callback)
btn2 = Button(text='Hello world 2')
btn2.bind(on_press=callback)

class PongApp(App):
    def build(self):
        return btn2


if __name__ == '__main__':
    PongApp().run()