import unittest
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from funcoes import *
from login_screen import LoginScreen
from home_screen import HomeScreen
from create_screen import CreateScreen
from createcompany_screen import CreateCompany
from createuser_screen import CreateUser


Builder.load_file('home_screen.kv')
Builder.load_file('login_screen.kv')
Builder.load_file('create_screen.kv')
Builder.load_file('createcompany_screen.kv')
Builder.load_file('createuser_screen.kv')



def create_screen_manager():
    sm = ScreenManager()
    sm.add_widget(HomeScreen(name='home'))
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(CreateScreen(name='create'))
    sm.add_widget(CreateCompany(name='createcompany'))
    sm.add_widget(CreateUser(name='createuser'))




    return sm

class MainApp(App):
    def build(self):
        return create_screen_manager()

if __name__ == '__main__':
    #unittest.main()
    MainApp().run()