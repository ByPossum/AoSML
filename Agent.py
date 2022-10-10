import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, Flatten, Input

def MakeAgent(width, height):
    model = Sequential()
    model.add(Input(shape=(width, height, 1)))
    model.add(Conv2D(filters=16, kernel_size=(3, 3), strides=(1,1), activation="relu"))
    model.add(Conv2D(filters=16, kernel_size=(5, 5), strides=(1,1), activation="relu"))
    model.add(Conv2D(filters=16, kernel_size=(7, 7), strides=(1,1), activation="relu"))
    model.add(Flatten())
    model.add(Dense(units=256, activation="relu"))
    model.add(Dense(units=128, activation="relu"))
    model.add(Dense(units=4, activation="sigmoid"))
    model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
    return model