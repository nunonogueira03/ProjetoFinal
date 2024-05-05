from kivy.uix.screenmanager import Screen
import funcoes
from kivy.app import App

class LoginScreen(Screen):
        def go_to_home_screen(self):
        # Método para ir para a tela de criar conta
            App.get_running_app().root.current = 'home'

        def do_login(self, username, password):
        # Aqui você adicionaria a lógica para verificar as credenciais
            if username == "admin" and password == "admin":
                print("Login bem-sucedido!")
                App.get_running_app().root.current = 'next_screen_name'
            else:
                print("Falha no login!")
        pass