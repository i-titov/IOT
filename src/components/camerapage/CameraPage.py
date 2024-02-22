import cv2
import numpy as np
import sqlite3
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.app import App

# Create a SQLite database connection
conn = sqlite3.connect('video_stream.db')
c = conn.cursor()

# Create a table to store video frames
c.execute('''CREATE TABLE IF NOT EXISTS frames (id INTEGER PRIMARY KEY, frame BLOB)''')
conn.commit()


class CameraPage(Screen):
    def __init__(self, **kwargs):
        super(CameraPage, self).__init__(**kwargs)

        self.camera = Camera(play=True, index=0)  # Use the default camera (index=0)
        self.start_button = Button(text='Start Streaming', size_hint=(None, None), size=(200, 40), on_press=self.start_streaming)
        self.stop_button = Button(text='Stop Streaming', size_hint=(None, None), size=(200, 40), on_press=self.stop_streaming)

        layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 250), spacing=10)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Center the layout
        layout.add_widget(self.camera)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        self.add_widget(layout)

        self.is_streaming = False

    def start_streaming(self, instance):
        if not self.is_streaming:
            self.is_streaming = True
            self.capture_video()

    def stop_streaming(self, instance):
        self.is_streaming = False

    def capture_video(self):
        while self.is_streaming:
            # Capture frame from camera
            ret, frame = self.camera.texture.to_image()
            if ret:
                # Convert frame to byte array
                frame_bytes = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR))[1].tobytes()

                # Save frame in database
                c.execute('''INSERT INTO frames (frame) VALUES (?)''', (frame_bytes,))
                conn.commit()


class VideoStreamApp(App):
    def build(self):
        return CameraPage()


if __name__ == '__main__':
    VideoStreamApp().run()

# Close database connection when the application stops
conn.close()
