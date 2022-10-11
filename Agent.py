import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, Flatten, Input, Reshape
from rl.agents import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

def MakeModel(width, height):
    model = Sequential()
    model.add(Input(shape=(1, width, height, 1)))
    model.add(Conv2D(filters=16, kernel_size=(3, 3), strides=(1,1), activation="relu"))
    model.add(Conv2D(filters=16, kernel_size=(5, 5), strides=(1,1), activation="relu"))
    model.add(Conv2D(filters=16, kernel_size=(7, 7), strides=(1,1), activation="relu"))
    model.add(Flatten())
    model.add(Dense(units=256, activation="relu"))
    model.add(Dense(units=128, activation="relu"))
    model.add(Dense(units=4, activation="sigmoid"))
    #model.add(Reshape((4, 1)))
    return model

def MakeAgent(model, actions, lim):
    mem = SequentialMemory(limit=lim, window_length=1, ignore_episode_boundaries=True)
    agent = DQNAgent(model=model, policy=EpsGreedyQPolicy(), memory=mem, nb_actions=actions, nb_steps_warmup=10, target_model_update=50)
    return agent