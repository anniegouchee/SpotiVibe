from flask import Flask, render_template, send_from_directory
import tensorflow as tf
from flask_socketio import SocketIO, emit
import base64, os, cv2
import numpy as np
from song_recommender import recommend_songs_for_mood
import config

FACE_DETECTION_XML = config.FACE_DETECTION_XML
MODEL_COMPILATION = tf.keras.models.load_model(config.MODEL_COMPILATION)
SPOTIFY_TOKEN = config.SPOTIFY_TOKEN
mood_dict = ["angry", "tried", "fear", "happy", "sad", "excited", "neutral"]


def detect_mood(frame):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + FACE_DETECTION_XML)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    face_roi = None
    for x, y, w, h in faces:
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        facess = faceCascade.detectMultiScale(roi_gray)
        if len(facess) == 0:
            print("Face not detected")
        else:
            for ex, ey, ew, eh in facess:
                face_roi = roi_color[ey : ey + eh, ex : ex + ew]
    if face_roi is not None:
        final_image = cv2.resize(face_roi, (224, 224))
        final_image = np.expand_dims(final_image, axis=0)
        final_image = final_image / 255.0
        Predictions = MODEL_COMPILATION.predict(final_image)

        status = mood_dict[np.argmax(Predictions)]
        recommended_songs = recommend_songs_for_mood(status, SPOTIFY_TOKEN)
        return recommended_songs, status


app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return render_template("index.html")


def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})


@socketio.on("image")
def receive_image(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)
    print(detect_mood(image))


if __name__ == "__main__":
    socketio.run(app, debug=True, port=4999, host="0.0.0.0")
