from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import FadeTransition, SlideTransition


class CustomScreen(Screen):
    def __init__(self, **kwargs):
        super(CustomScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # RGB para branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        #self.transition = SlideTransition(direction='left', duration=0)
    

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos