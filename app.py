from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.components.login.LoginPage import LoginPage
from src.components.camerapage.CameraPage import CameraPage



class MyApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(LoginPage(name='login_page'))
        sm.add_widget(CameraPage(name='camera_page'))
        return sm


if __name__ == '__main__':
    MyApp().run()