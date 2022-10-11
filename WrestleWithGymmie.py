import gym
import Application
from gym import Env, spaces
import numpy

class WrestleWithGymmie(Env):
    def __init__(self, app, width, height, legalMove):
        self.actions = spaces.Box(low=0, high=1, shape=(4, 1), dtype=float)
        self.observe = spaces.Box(low=0, high=5, shape=(width, height, 1), dtype=float)
        self.reward = 0
        self.movesMade = 0
        self.app = app
        self.legalMove = legalMove
        self.maxTries = (width*height)*0.5

    def reset(self):
        self.app.ResetBaybee()
        self.reward = 0
        self.movesMade = 0
        return self.app.GetMap()

    def step(self, action):
        index = numpy.argmax(action)
        self.app.TranslatePlayerMove(self.legalMove[index])
        self.app.GameplayLoop()
        world = self.app.GetMap()
        self.movesMade += 1
        self.reward = -(self.app.DistanceToGoal()**2)*0.1

        end = self.app.CheckDone()
        info = {}
        if self.movesMade > self.maxTries:
            end = True
        return world, self.reward, end, info

    def render(self):
        self.app.RenderLoop()
        return self.app.GetMap()
