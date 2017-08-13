from random import randint

from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, ObjectProperty
from kivy.uix import layout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.vector import Vector
import analyze


def callback(instance):
    print(instance)

class dndUI(BoxLayout):
    def __int__(self,**kwargs):
        super(dndUI,self).__init__(**kwargs)



class dndUIApp(App):
    def __int__(self,**kwargs):
        super(dndUIApp,self).__init__(**kwargs)

    def build(self):
        return dndUI()



if __name__ == '__main__':
    dndUIApp().run()