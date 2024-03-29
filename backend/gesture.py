# SNIPPET OF CODE TO COPY TO APP.PY WHEN FRONTEND FINISHED

from flask import Flask, render_template, send_from_directory
import tensorflow as tf
from flask_socketio import SocketIO, emit
import base64, os, cv2
import numpy as np
from song_recommender import recommend_songs_for_mood
import config, face_recognition
import mediapipe as mp

FACE_DETECTION_XML = config.FACE_DETECTION_XML
MODEL_COMPILATION = tf.keras.models.load_model(config.MODEL_COMPILATION)
global_spotify_token = config.SPOTIFY_TOKEN
mood_dict = ["angry", "excited", "happy", "neutral", "sad", "tired"]

mood_history = {
    "angry": 0,
    "excited": 0,
    "happy": 0,
    "neutral": 0,
    "sad": 0,
    "tired": 0,
    "total": 0,
}


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
        # recommended_songs = recommend_songs_for_mood(status, global_spotify_token)
        return status  # , recommended_songs


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


def is_skip_gesture(hand_landmarks):
    # Implement your song skip gesture recognition logic here
    # Example: Check if the thumb tip is to the left of the index finger tip
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[
        mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP
    ]
    return thumb_tip.x < index_finger_tip.x


def is_open_palm(hand_landmarks):
    palm_landmarks_indices = [0, 5, 9, 13, 17]

    distances = [
        hand_landmarks.landmark[i].x
        - hand_landmarks.landmark[i - 1].x
        + hand_landmarks.landmark[i].y
        - hand_landmarks.landmark[i - 1].y
        + hand_landmarks.landmark[i].z
        - hand_landmarks.landmark[i - 1].z
        for i in palm_landmarks_indices
    ]

    threshold = 0.1
    return all(d < threshold for d in distances)


def is_closed_fist(hand_landmarks):
    thumb_tip_index = mp.solutions.hands.HandLandmark.THUMB_TIP.value
    finger_tip_indices = [
        mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP.value,
        mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP.value,
        mp.solutions.hands.HandLandmark.RING_FINGER_TIP.value,
        mp.solutions.hands.HandLandmark.PINKY_TIP.value,
    ]

    distances = [
        hand_landmarks.landmark[thumb_tip_index].x
        - hand_landmarks.landmark[i].x
        + hand_landmarks.landmark[thumb_tip_index].y
        - hand_landmarks.landmark[i].y
        + hand_landmarks.landmark[thumb_tip_index].z
        - hand_landmarks.landmark[i].z
        for i in finger_tip_indices
    ]

    threshold = 0.1

    return all(d > threshold for d in distances)


@socketio.on("image")
def receive_image(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)
    # mood, recommended_songs = detect_mood(image)
    # mood = detect_mood(image)
    # if mood:
    #     mood_history[mood] += 1
    #     mood_history["total"] += 1
    #     mood_percentage = {
    #         "angry": 0,
    #         "excited": 0,
    #         "happy": 0,
    #         "neutral": 0,
    #         "sad": 0,
    #         "tired": 0,
    #         "total": 0,
    #     }
    #     total = mood_history["total"]
    #     for key in mood_history.keys():
    #         if key == "total":
    #             continue
    #         mood_percentage[key] = mood_history[key] / total
    #     print(mood_percentage)
    # emit(
    #     "analysis_result",
    #     {
    #         "mood": mood,
    #         # "songs": recommended_songs,
    #         "moodPercentage": mood_percentage,
    #     },
    # )

    mp_hands = mp.solutions.hands

    capture = image

    with mp_hands.Hands(
        min_detection_confidence=0.8, min_tracking_confidence=0.5
    ) as hands:
        frame = capture
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_image = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if detected_image.multi_hand_landmarks:
            for landmarks in detected_image.multi_hand_landmarks:
                #         mp_drawing.draw_landmarks(
                #             image,
                #             hand_lms,
                #             mp_hands.HAND_CONNECTIONS,
                #             landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                #                 color=(255, 0, 255), thickness=4, circle_radius=2
                #             ),
                #             connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                #                 color=(20, 180, 90), thickness=2, circle_radius=2
                #             ),
                #         )
                # for

                if is_open_palm(landmarks):
                    print("skip")

                if is_closed_fist(landmarks):
                    print("pause")


@socketio.on("spotify_token")
def receive_token(spotify_token):
    print(spotify_token)
    global global_spotify_token
    global_spotify_token = spotify_token


# CODE FOR FACIAL_RECOGNITION
known_face_encodings = []
known_face_names = []


@socketio.on("store")
def store_face(args: dict):
    """
    args:
        image: dict
    """
    image = args["image"]
    user = args["user"]
    image = base64_to_image(image)
    path = os.path.join(os.curdir(), f"{user}.jpg")
    cv2.imwrite(path, image)
    known_image = face_recognition.load_image_file(path)
    img_encoding = face_recognition.face_encodings(known_image)[0]
    known_face_encodings.append(img_encoding)
    known_face_names.append(user)


@socketio.on("recognize")
def find_face(frame):
    """
    args:
        frame:
            finds faces from existing fraces in the db
    """
    face_locations = []
    face_encodings = []
    face_names = []
    # frame = cv2.imread(frame)
    frame = base64_to_image(frame)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    print(face_locations)
    face_encodings = face_recognition.face_encodings(np.array(rgb_small_frame))

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)

        # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(
            frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
    # cv2.imshow("Video", frame)
    emit({"names": face_names, "image": frame})


if __name__ == "__main__":
    socketio.run(app, debug=True, port=4999, host="0.0.0.0")
