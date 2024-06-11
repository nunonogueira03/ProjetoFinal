from kivy.uix.screenmanager import Screen
import funcoes
from kivy.app import App


class PreFraction(Screen):
    def go_to_create_account(self):
        # Método para ir para a tela de criar conta
        App.get_running_app().root.current = 'create'

    def go_to_login(self):
        # Método para ir para a tela de login
        App.get_running_app().root.current = 'login'
    pass