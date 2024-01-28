
# SNIPPET OF CODE TO COPY TO APP.PY WHEN FRONTEND FINISHED

def is_open_palm(hand_landmarks):

    palm_landmarks_indices = [0, 5, 9, 13, 17]


    distances = [
        hand_landmarks.landmark[i].x
        
hand_landmarks.landmark[i - 1].x+ hand_landmarks.landmark[i].y
hand_landmarks.landmark[i - 1].y+ hand_landmarks.landmark[i].z
hand_landmarks.landmark[i - 1].z
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
        
hand_landmarks.landmark[i].x+ hand_landmarks.landmark[thumb_tip_index].y
hand_landmarks.landmark[i].y+ hand_landmarks.landmark[thumb_tip_index].z
hand_landmarks.landmark[i].z
  for i in finger_tip_indices
]

    threshold = 0.1

    return all(d > threshold for d in distances)

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