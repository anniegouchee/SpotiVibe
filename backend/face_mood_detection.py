import tensorflow as tf
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

import cv2

from song_recomender import recommend_songs_for_mood

path = "haarcascade_frontalface_default.xml"
font_scale = 1.5
font = cv2.FONT_HERSHEY_PLAIN

rectangle_bgr = (255, 255, 255)
img = np.zeros((500, 500))
text = "Some text in a box"
(text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
text_offset_x = 10
text_offset_y = img.shape[0] -25
box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height -2))
cv2.rectangle(img, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0,0,0), thickness=1)

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

mood_dict = {0:"angry", 1:"tried", 2:"fear", 3:"happy", 4:"sad", 5:"excited", 6:"neutral"}
while True: 
    ret, frame = cap.read()
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.1,4)
    cv2.imwrite('image.png', frame)
    face_roi = None
    for x,y,w,h in faces: 
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0,0), 2)
        facess = faceCascade.detectMultiScale(roi_gray)
        if len(facess) == 0:
            print("Face not detected")
        else:
            for (ex, ey, ew, eh) in facess:
                face_roi = roi_color[ey: ey+eh, ex:ex + ew]
    if face_roi is not None:
        final_image = cv2.resize(face_roi, (224,224))
        final_image = np.expand_dims(final_image, axis =0)
        final_image=final_image/255.0
        font = cv2.FONT_HERSHEY_SIMPLEX
        new_model = tf.keras.models.load_model('mod_empathly_model_94p24.h5')
        Predictions = new_model.predict(final_image)
        
        font_scale = 1.5
        font = cv2.FONT_HERSHEY_PLAIN

        status = mood_dict[np.argmax(Predictions)]
        recommended_songs = recommend_songs_for_mood(status, 'BQCOnfhjyZPk05l7iLLflFvqp2vN4KndvjJ_BUeBwHJbPU1OuOPp3H8pbAcKhAmzsk1jVJDzYFqyYBfYVOObd3jWFAno7C9KjIapOIaBa4NisePpEBjTyGdz9rjahWUJ_Me5hG6HTW_vz9RtBLU9DNvWtpbB5_5td7dLpJ8930R9XORjfgdnT9VRIHlJhc_ZYiEK5kCTke225lFq8LLcdJDr7qfDKsKTZpMdznl4IC1_j_fADiaYFJ2aREUHL4pcu5LFpBtZB-IxGqfbmE3eKO7B')
        x1,y1,w1,h1 = 0, 0, 175, 75
        cv2.rectangle(frame, (x1,x1), (x1+w1,y1+h1), (0,0,0), -1)
        cv2.putText(frame, status, (x1 +int(w1/10), y1+int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.putText(frame, status, (100, 150), font, 3, (0,0,255),2,cv2.LINE_4)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255))
        start_x, start_y = 10, 200
        spacing = 30
        cv2.putText(frame, str(recommended_songs), (start_x, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imshow('Face Emotion Recognition', frame)
        
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()