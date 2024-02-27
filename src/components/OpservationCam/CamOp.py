import cv2
from pymongo import MongoClient
import numpy as np
import io
import time
import requests

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['ivan']
collection = db['videos']

# Configuration de la capture vidéo
cap = cv2.VideoCapture(0)  # Vous pouvez également spécifier le chemin d'un fichier vidéo

# Configuration du serveur
server_url = 'http://example.com/upload'  # Remplacez par l'URL de votre serveur
server_endpoint = '/upload_video'
headers = {'Content-Type': 'application/octet-stream'}

# Temps actuel
start_time = time.time()
capture_duration = 1 * 60  # 5 minutes

while True:
    # Capture d'une image depuis la webcam
    ret, frame = cap.read()

    # Affichage de la vidéo en direct
    cv2.imshow('Video Capture', frame)

    # Enregistrement de la vidéo dans la base de données MongoDB
    encoded_frame = cv2.imencode('.jpg', frame)[1]
    video_data = io.BytesIO(encoded_frame)
    video_binary = video_data.getvalue()

    # Insertion du frame dans la base de données
    collection.insert_one({'video': video_binary})

    # Vérification du temps écoulé
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Arrêter la capture après la durée spécifiée
    if elapsed_time >= capture_duration:
        print("Capture duration reached. Stopping video capture.")
        break

    # Sortie de la boucle avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Envoi de la vidéo au serveur
response = requests.post(f'{server_url}{server_endpoint}', data=video_binary, headers=headers)
print(f"Video sent to server. Response: {response.status_code}")

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
