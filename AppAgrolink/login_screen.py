from kivy.uix.screenmanager import Screen
from funcoes import *
from kivy.app import App
from kivy.properties import ListProperty  # Import necessário para propriedades de lista
import json



class LoginScreen(Screen):
        
        nomes_empresas = ListProperty([])
    
        def __init__(self, **kwargs):
            super(LoginScreen, self).__init__(**kwargs)
            self.nomes_empresas = []  # Inicializa como lista vazia, certifique-se de que o nome está correto


        def on_enter(self):
            super(LoginScreen, self).on_enter()
            # Obter a string JSON das empresas
            empresas_json = nome_empresas()
            # Converter a string JSON de volta para uma lista Python
            self.nomes_empresas = json.loads(empresas_json)

        def update_empresas(self):
            self.empresa_values = nome_empresas()

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