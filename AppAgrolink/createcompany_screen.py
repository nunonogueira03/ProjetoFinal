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

    def criar(self):
        nomeempresa = self.ids.nomeempresa.text
        numerocontribuinte = self.ids.numerocontribuinte.text
        morada = self.ids.morada.text
        numerocontacto = self.ids.contacto.text
        paiscontacto = self.ids.paiscontacto.text

        contacto = paiscontacto+numerocontacto

        mensagens_erro = []

                    # Guardar os dados na base de dados
        dados_empresa = {'nome' :nomeempresa, 
                            'numerocontribuinte' :numerocontribuinte, 
                            'morada':morada,
                            'contacto':contacto}
        
        adicionar_empresa(dados_empresa)

    def mostrar_popup_erro(self, mensagens):
        content = BoxLayout(orientation='vertical')
        for mensagem in mensagens:
            content.add_widget(Label(text=mensagem))
        close_button = Button(text='Fechar', size_hint=(1, 0.2))
        content.add_widget(close_button)
        popup = Popup(title='Erro ao criar Empresa',
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
        self.manager.current = 'firstapppage'    

    def go_to_home_screen(self):
        # Método para ir para a tela de criar conta
            App.get_running_app().root.current = 'create_screen'

    pass