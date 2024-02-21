from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.camera import Camera


class CameraPage(Screen):
    def __init__(self, **kwargs):
        super(CameraPage, self).__init__(**kwargs)

        self.camera = Camera(play=True)

        layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 250))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Center the layout
        layout.add_widget(Label(text='Camera Page', font_size=20))
        layout.add_widget(self.camera)
        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(200, 40), on_press=self.go_back))
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'login_page'


# Set the background color
Window.clearcolor = (0.2, 0.7, 0.5, 1)  # RGBA
