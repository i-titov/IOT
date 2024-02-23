from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.app import App
import cv2
import sqlite3
import os
import numpy as np
import time

class CameraPage(Screen):
    def __init__(self, **kwargs):
        super(CameraPage, self).__init__(**kwargs)

        # Initialisation de la caméra et des boutons
        self.camera = Camera(play=True, index=0, resolution=(800, 600))
        self.start_stream_button = Button(text='Start Streaming', size_hint=(None, None), size=(200, 40),
                                          on_press=self.start_streaming,
                                          background_color=(0, 0.7, 0.3, 1),  # Couleur du fond en RVBA (0-1)
                                          color=(1, 1, 1, 1))  # Couleur du texte en RVBA (0-1)

        self.stop_stream_button = Button(text='Stop Streaming', size_hint=(None, None), size=(200, 40),
                                         on_press=self.stop_streaming,
                                         background_color=(0.7, 0, 0.3, 1),
                                         color=(1, 1, 1, 1))

        self.start_record_button = Button(text='Start Recording', size_hint=(None, None), size=(200, 40),
                                          on_press=self.start_recording,
                                          background_color=(0, 0.3, 0.7, 1),
                                          color=(1, 1, 1, 1))

        self.stop_record_button = Button(text='Stop Recording', size_hint=(None, None), size=(200, 40),
                                         on_press=self.stop_recording,
                                         background_color=(0.7, 0, 0, 1),
                                         color=(1, 1, 1, 1))

        # Configuration de la mise en page
        layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(600, 480), spacing=10)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        layout.add_widget(self.camera)
        layout.add_widget(self.start_stream_button)
        layout.add_widget(self.stop_stream_button)
        layout.add_widget(self.start_record_button)
        layout.add_widget(self.stop_record_button)
        self.add_widget(layout)

        # Initialisation des variables et de la base de données
        self.is_streaming = False
        self.is_recording = False
        self.conn = sqlite3.connect('video_stream.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS frames (id INTEGER PRIMARY KEY, frame BLOB)''')
        self.conn.commit()

        # Initialisation de l'enregistreur vidéo
        self.video_recorder = VideoRecorder()

    def start_streaming(self, instance):
        # Démarrer le streaming
        if not self.is_streaming:
            self.is_streaming = True
            self.capture_video()

    def stop_streaming(self, instance):
        # Arrêter le streaming
        self.is_streaming = False

    def start_recording(self, instance):
        # Démarrer l'enregistrement vidéo
        if not self.is_recording:
            self.is_recording = True
            self.video_recorder.start_recording()

    def stop_recording(self, instance):
        # Arrêter l'enregistrement vidéo
        self.is_recording = False
        self.video_recorder.stop_recording()

    def capture_video(self):
        # Capturer la vidéo
        while self.is_streaming:
            ret, frame = self.camera.texture.to_image()
            if ret:
                resized_frame = self.resize_image(frame.pixels, target_size=(800, 600))
                frame_bytes = cv2.imencode('.jpg', cv2.cvtColor(resized_frame, cv2.COLOR_RGBA2BGR))[1].tobytes()

                # Insérer le frame dans la base de données
                self.c.execute('''INSERT INTO frames (frame) VALUES (?)''', (sqlite3.Binary(frame_bytes),))
                self.conn.commit()
                cv2.imshow('Camera', cv2.cvtColor(resized_frame, cv2.COLOR_RGBA2BGR))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def resize_image(self, image, target_size):
        # Redimensionner l'image
        return cv2.resize(image, target_size)

    def on_leave(self, *args):
        # Fermer la connexion à la base de données lorsqu'on quitte la page
        self.conn.close()

class VideoRecorder:
    def __init__(self):
        # Initialisation de l'enregistreur vidéo
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.output_folder = os.path.join(desktop_path, 'recorded_videos')

        # Vérifier si le dossier de destination existe, sinon le créer
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.recording = False
        self.video_writer = None
        self.start_time = None

    def start_recording(self):
        # Démarrer l'enregistrement vidéo
        self.recording = True
        video_filename = f'output_video_{time.strftime("%Y%m%d_%H%M%S")}.mp4'
        video_path = os.path.join(self.output_folder, video_filename)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_width = 800  # Vous pouvez ajuster la largeur et la hauteur selon vos besoins
        frame_height = 600
        self.video_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (frame_width, frame_height))
        self.start_time = time.time()

    def stop_recording(self):
        # Arrêter l'enregistrement vidéo
        if self.recording:
            self.recording = False
            self.video_writer.release()

    def record(self):
        # Enregistrement vidéo
        while True:
            # Simulez ici la récupération du frame depuis la caméra
            frame = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)

            if self.recording:
                self.video_writer.write(frame)
                current_time = time.time()
                elapsed_time = current_time - self.start_time
                if elapsed_time >= 1 * 60:
                    print("Arrêt automatique après 1 minute.")
                    self.stop_recording()
                    break

            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

class VideoStreamApp(App):
    def build(self):
        return CameraPage()

    def on_start(self):
        # Démarrer l'enregistrement automatiquement au lancement de l'application
        self.root.start_recording(None)

if __name__ == '__main__':
    VideoStreamApp().run()
