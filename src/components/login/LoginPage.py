from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)

        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint=(None, None), size=(200, 40))
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False, size_hint=(None, None), size=(200, 40))
        self.login_button = Button(text='Login', size_hint=(None, None), size=(200, 40))
        self.login_button.bind(on_press=self.login)

        layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 200))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Center the layout
        layout.add_widget(Label(text='Sign in', font_size=20))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)
        self.add_widget(layout)

    def show_spinner(self, instance):
        self.spinner.active = True  # Show spinner
        Clock.schedule_once(self.login, 2)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        self.manager.current = 'camera_page'  # Switch to another screen

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YourAccessTokenHere'
        }

        # Make a POST request to the server
        url = 'http://server/login'
        data = {'username': username, 'password': password}
        #response = requests.post(url, json=data, headers=headers)
        self.manager.current = 'camera_page'  # Switch to camera page

        #if response.status_code == 200:
           # print("Login successful!")
        #else:
         #   print("Invalid username or password")
          #  self.spinner.active = False

Window.clearcolor = (0.2, 0.7, 0.5, 1)