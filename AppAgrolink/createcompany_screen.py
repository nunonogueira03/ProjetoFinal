from kivy.uix.screenmanager import Screen
from funcoes import *
from kivy.app import App
import json



class CreateCompany(Screen):

    def __init__(self, **kwargs):
        super(CreateCompany, self).__init__(**kwargs)   


    def go_to_home_screen(self):
        # Método para ir para a tela de criar conta
            App.get_running_app().root.current = 'create'

    pass