from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from funcoes import *
from kivy.app import App
import json
from kivy.properties import ListProperty, BooleanProperty  # Import necessário para propriedades de lista
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class ValidateUsers(Screen):

    def mostrar_popup_erro(self, titulo, mensagem, botao):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=mensagem))
        close_button = Button(text=botao, size_hint=(1, 0.2))
        content.add_widget(close_button)
        popup = Popup(title=titulo,
                      content=content,
                      size_hint=(0.6, 0.3))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def on_enter(self):
        # Executar servico para verificar utilizadores por validar
        self.ids.selectButton.text == 'Selecionar Todos'
        success, lista_utilizadores = utilizadores_verificar()  

        if not success:
            App.get_running_app().root.current = 'home'      
            self.mostrar_popup_erro('Sessão Expirada',"Faça login novamente.","Fechar")
        
        if not lista_utilizadores:
            App.get_running_app().root.current = 'firstapppage'      
            self.mostrar_popup_erro('',"Sem novos utilizadores","Voltar")

        print("USERSSSS:")
        print(lista_utilizadores)

        # Inicializa o side_panel como oculto e o scroll_content desativado
        icons = "account-circle"
        for email in lista_utilizadores:
            self.ids.scroll.add_widget(
                ListItemWithCheckbox(text=email, icon=icons))
            
    def on_leave(self):
        self.ids.scroll.clear_widgets()
        #self.ids.selectButton.text = 'Selecionar Todos'
            
    def autorizar(self):
        for child in self.ids.scroll.children:
            print(child.text,'with', child.icon,'is',child.ids.rcbox.active)
        
        listaAutorizar = [child.text for child in self.ids.scroll.children if child.ids.rcbox.active]
        if listaAutorizar:
            autorizarutilizadores(listaAutorizar)
        self.ids.selectButton.text = 'Selecionar Todos'
        App.get_running_app().root.current = 'firstapppage'


    def selectall(self):
        newText = "Remover Seleção" if self.ids.selectButton.text == 'Selecionar Todos' else "Selecionar Todos"
        valueToAll = self.ids.selectButton.text == 'Selecionar Todos'
        for child in self.ids.scroll.children: 
            child.ids.rcbox.active = valueToAll
        
        self.ids.selectButton.text = newText

    def go_to_create_account(self):
        # Método para ir para a tela de criar conta
        App.get_running_app().root.current = 'createuser'

    def go_to_login(self):
        # Método para ir para a tela de login
        App.get_running_app().root.current = 'login'

