from kivy.uix.screenmanager import Screen
from funcoes import *
from kivy.app import App
import json



class CreateScreen(Screen):

    def go_to_create_account(self):
        # Método para ir para a tela de criar conta
        App.get_running_app().root.current = 'createcompany'

    def go_to_login(self):
        # Método para ir para a tela de login
        App.get_running_app().root.current = 'createuser'

    pass