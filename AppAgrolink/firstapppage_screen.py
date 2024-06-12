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
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker, MapSource, MarkerMapLayer, MapLayer
from kivy.graphics import Color, Line, Bezier, Ellipse, Triangle

class LineMapLayer(MapLayer):
    def __init__(self, points_func, **kwargs):
        super().__init__(**kwargs)
        self.points_func = points_func

    def reposition(self):
        self.draw_line()

    def draw_line(self):
        self.canvas.clear()
        points = self.points_func()
        with self.canvas:
            Color(0, 0, 0, 0.9)  # Linha vermelha
            Line(points=points, width=2)

class FirstAppPage(Screen):

    def reposition(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0)  # Linha vermelha
            Line(points=self.points, width=2)

    def on_enter(self):
        super(FirstAppPage, self).on_enter()

        # Inicializa o side_panel como oculto e o scroll_content desativado
        self.ids.main_map.zoom = 17
        self.ids.main_map.center_on(40.20749225876448, -8.452005896749045)

        # Obtém os dados em formato JSON
        pontos_json = listapontos()
        # Converte o JSON de volta para uma lista de dicionários
        pontos = json.loads(pontos_json)

        for ponto in pontos:
            print(f"Adding point: {ponto}")  # Depuração
            self.ponto = MapMarkerPopup(lat=ponto['latitude'], lon=ponto['longitude'], source='assets/points24.png')
            self.ids.main_map.add_widget(self.ponto)

        self.sensor = MapMarkerPopup(lat=40.20810427464019, lon=-8.451462148859271, source='assets/sensor24.png')
        self.label = Label(text="Sensor Info", size=(self.width * 0.2, self.height * 0.05), pos=(self.sensor.pos[0], self.sensor.pos[1]))
        self.sensor.add_widget(self.label)
        self.ids.main_map.add_widget(self.sensor)
        
        # Adiciona pontos de teste
        self.pontoteste1 = MapMarkerPopup(lat=40.20766269503174, lon=-8.452334840900821, source='assets/points24.png')
        self.ids.main_map.add_widget(self.pontoteste1)

        self.pontoteste2 = MapMarkerPopup(lat=40.20745756204344, lon=-8.45099810157657, source='assets/points24.png')
        self.ids.main_map.add_widget(self.pontoteste2)

        # Adiciona a linha entre os dois pontos
        self.line_layer = LineMapLayer(points_func=self.get_line_points)
        self.ids.main_map.add_layer(self.line_layer)

        # Vincula eventos on_size e on_pos para reposicionar a linha quando o mapa for redimensionado ou movido
        self.ids.main_map.bind(on_size=self.update_line, on_pos=self.update_line, on_zoom=self.update_line)

    def get_line_points(self):
        p1 = self.ids.main_map.get_window_xy_from(lat=self.pontoteste1.lat, lon=self.pontoteste1.lon, zoom=self.ids.main_map.zoom)
        p2 = self.ids.main_map.get_window_xy_from(lat=self.pontoteste2.lat, lon=self.pontoteste2.lon, zoom=self.ids.main_map.zoom)
        return [p1[0], p1[1], p2[0], p2[1]]

    def update_line(self, *args):
        self.line_layer.reposition()

    def mostrar(self, instance):
        self.label.text = "Sensor Clicked:\nLatitude: 40.20810427464019\nLongitude: -8.451462148859271"

    def go_to_create_account(self):
        # Método para ir para a tela de criar conta
        App.get_running_app().root.current = 'createuser'

    def go_to_login(self):
        # Método para ir para a tela de login
        App.get_running_app().root.current = 'login'