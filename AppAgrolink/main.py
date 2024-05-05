from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from funcoes import *
from login_screen import LoginScreen
from home_screen import HomeScreen

Builder.load_file('home_screen.kv')
Builder.load_file('login_screen.kv')

def create_screen_manager():
    sm = ScreenManager()
    sm.add_widget(HomeScreen(name='home'))
    sm.add_widget(LoginScreen(name='login'))
    return sm

class MainApp(App):
    def build(self):
        return create_screen_manager()

if __name__ == '__main__':
    MainApp().run()