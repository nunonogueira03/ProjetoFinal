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



class CreateUser(Screen):

    nomes_empresas = ListProperty([])

    def __init__(self, **kwargs):
        super(CreateUser, self).__init__(**kwargs)   
        self.nomes_empresas = []  # Inicializa como lista vazia, certifique-se de que o nome está correto

    def on_enter(self):
        super(CreateUser, self).on_enter()
        # Obter nome das empresas
        self.nomes_empresas = nome_empresas()

    def update_empresas(self):
        self.empresa_values = nome_empresas()

    def validar_inputs(self):
        nome_empresa = self.ids.empresa_spinner.text
        numfuncionario = self.ids.numfuncionario_input.text
        nome = self.ids.nome_input.text
        password = self.ids.input1.text
        password2 = self.ids.input2.text
        email = self.ids.email_input.text

        mensagens_erro = []

        if not password == password2:
            mensagens_erro.append("As senhas são diferentes!")
        if not validar_email(email):
            mensagens_erro.append("E-mail inválido!")

        if mensagens_erro:
            self.mostrar_popup_erro(mensagens_erro)
        else:
            # Guardar os dados na base de dados
            dados_utilizador = {'nome' :nome, 
                                'password' :password, 
                                'numfuncionario':numfuncionario, 
                                'email':email, 
                                'nome_empresa':nome_empresa}
            sucesso, mensagem = adicionar_utilizador(dados_utilizador)
            if sucesso:
                self.mostrar_popup_sucesso(mensagem)
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

    def mostrar_popup_sucesso(self, mensagem):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=mensagem))
        close_button = Button(text='Fechar', size_hint=(1, 0.2))
        content.add_widget(close_button)
        popup = Popup(title='Sucesso',
                      content=content,
                      size_hint=(0.8, 0.4))
        close_button.bind(on_release=lambda *args: self.ir_para_proxima_tela(popup))
        popup.open()

    def ir_para_proxima_tela(self, popup):
        popup.dismiss()
        self.manager.current = 'home'

    def go_to_home_screen(self):
        # Método para ir para a tela de criar conta
            App.get_running_app().root.current = 'create'

    pass