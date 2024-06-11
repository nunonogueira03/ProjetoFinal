from kivy.uix.screenmanager import Screen
from funcoes import *
from kivy.app import App
import json
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from funcoes import *
from kivy.app import App
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker, MapSource, MarkerMapLayer



class CreateCompany(Screen):

    def __init__(self, **kwargs):
        super(CreateCompany, self).__init__(**kwargs)   


    def go_to_home_screen(self):
        # Método para ir para a tela de criar conta
            App.get_running_app().root.current = 'create_screen'

    pass