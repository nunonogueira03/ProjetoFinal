from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from funcoes import *
from kivy.app import App
import json
from kivy.properties import ListProperty  # Import necessário para propriedades de lista
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class LoginScreen(Screen):
        

        nomes_empresas = ListProperty([])
    
        def __init__(self, **kwargs):
            super(LoginScreen, self).__init__(**kwargs)
            self.nomes_empresas = []  # Inicializa como lista vazia, certifique-se de que o nome está correto


        def on_enter(self):
            super(LoginScreen, self).on_enter()
            # Obter nome das empresas
            self.nomes_empresas = nome_empresas()

        #def on_leave(self):
        #    self.ids.password.text = 'Something special'

        def login(self):

            nome_empresa = self.ids.empresa_spinner.text
            password = self.ids.password.text
            email = self.ids.email_input.text    

            dados_utilizador = {'password': password,
                                    'email': email, 
                                    'nome_empresa': nome_empresa}
            sucesso, mensagem = login(dados_utilizador)
            if sucesso:

                #message = self.ids.input.text
                #screen_two = self.manager.get_screen('firstapppage')
                #screen_two.set_message(message)
                self.ids.email_input.text = ''
                self.ids.email_input.hint_text = 'Introduza o email'
                self.ids.password.text = ''
                self.ids.password.hint_text = 'Introduza a password'
                self.manager.current = 'firstapppage'
            else:
                self.mostrar_popup_erro([mensagem])
        
        def mostrar_popup_erro(self, mensagens):
            content = BoxLayout(orientation='vertical')
            for mensagem in mensagens:
                content.add_widget(Label(text=mensagem))
            close_button = Button(text='Fechar', size_hint=(1, 0.2))
            content.add_widget(close_button)
            popup = Popup(title='Erro de Validação',
                      content=content,
                      size_hint=(0.8, 0.4))
            close_button.bind(on_release=popup.dismiss)
            popup.open()

        def update_empresas(self):
            self.empresa_values = nome_empresas()

        def go_to_home_screen(self):
        # Método para ir para a tela de criar conta
            App.get_running_app().root.current = 'firstapppage'

        def do_login(self, username, password):
        # Aqui você adicionaria a lógica para verificar as credenciais
            if username == "admin" and password == "admin":
                print("Login bem-sucedido!")
                App.get_running_app().root.current = 'next_screen_name'
            else:
                print("Falha no login!")
        pass