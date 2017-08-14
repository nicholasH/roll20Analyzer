from random import randint

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import analyze




class dndUI(BoxLayout):


    def run(self):
        analyze.analyze()


class dndUIApp(App):
    def build(self):
        return dndUI()



if __name__ == '__main__':
    dndUIApp().run()