import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2, os, random

# import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from pillow_heif import register_heif_opener

DataDir = "../Emotions/"
# name of folder corresponds to the emotions
# Angry Disgust Fear Happy Sad Suprise Neutral
Classes = ["Angry", "Excited", "Happy", "Neutral", "Sad", "Tired"]

register_heif_opener()

for category in Classes:
    path = os.path.join(DataDir, category)
    print(path)
    for img in os.listdir(path):
        # Convert all images to .jpg
        if img[-4:] == "HEIC":
            with Image.open(os.path.join(path, img)) as image:
                img = img[:-4] + "jpg"
                # Convert to JPEG
                image.convert("RGB").save(f"{path}/{img}")
                # Remove original .HEIC image
                os.remove(f"{path}/{img[:-3]}HEIC")

train_data = []
img_size = 224


def training_data_generator():
    for category in Classes:
        path = os.path.join(DataDir, category)
        class_num = Classes.index(category)  ## only two columns for the class
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                new_array = cv2.resize(img_array, (img_size, img_size))
                train_data.append([new_array, class_num])
            except Exception as e:
                pass


training_data_generator()

temp = np.array(train_data)
random.shuffle(train_data)
X = []
y = []
for features, label in train_data:
    X.append(features)
    y.append(label)
X = np.array(X).reshape(-1, img_size, img_size, 3)

# create training data
X = []
y = []

for features, label in train_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, img_size, img_size, 3)  # converting it to 4 dimension

# Normalize
X = X / 255.0
Y = np.array(y)

# Pre-trained model
model = tf.keras.applications.MobileNetV2()
model.summary()
# Transfer Learning - Tuning weights will start from the last checkpoint
base_input = model.layers[0].input
# we convert the 1000 classes into 7 classes
base_output = model.layers[-2].output
# Adding a new layer after the output of global pulling layer
# Applying activation function
final_output = layers.Dense(128)(base_output)
final_output = layers.Activation("relu")(final_output)
final_output = layers.Dense(64)(final_output)
final_output = layers.Activation("relu")(final_output)
final_output = layers.Dense(7, activation="softmax")(
    final_output
)  # the classes went from 1000 to 7
# create a model
new_model = keras.Model(inputs=base_input, outputs=final_output)
new_model.summary()
new_model.compile(
    loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
)
# train the model
new_model.fit(X, Y, epochs=20)
