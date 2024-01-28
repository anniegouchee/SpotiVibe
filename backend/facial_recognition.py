import face_recognition, cv2
import numpy as np

known_face_encodings = []
known_face_names = []


def store_face(image: str, user: str):
    """
    args:
        image: str
            filepath to image
        user: str
            user/person associated with that image
    """
    known_image = face_recognition.load_image_file(image)
    img_encoding = face_recognition.face_encodings(known_image)[0]
    known_face_encodings.append(img_encoding)
    known_face_names.append(user)


def find_face(frame):
    """
    args:
        frame:
            finds faces from existing fraces in the db
    """
    face_locations = []
    face_encodings = []
    face_names = []
    frame = cv2.imread(frame)
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
    cv2.imshow("Video", frame)
    return face_names
