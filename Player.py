from SpriteFactory import SpriteFactory
from MapManager import MapMan
from consts import *

class Player:

    def __init__(self):
        self.sprite = SpriteFactory("Assets/Player.png")
        self.tileX = 0
        self.tileY = 0
        self.x = 0
        self.y = 0
        self.targetX = 0
        self.targetY = 0
        self.currentAction = None
        self.moveCheck = False

    def SetPos(self, x, y):
        self.tileX = x
        self.tileY = y
        self.SetTarget(self.tileX, self.tileY)

    def SetTarget(self, x, y):
        self.targetX = x * 32
        self.targetY = y * 32

    def UpdateRect(self):
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y

    def Move(self):
        if self.x < self.targetX:
            self.x += MOVESPEED
        elif self.x > self.targetX:
            self.x -= MOVESPEED
        if self.y < self.targetY:
            self.y += MOVESPEED
        elif self.y > self.targetY:
            self.y -= MOVESPEED
        self.UpdateRect()

    def MoveUp(self, map: MapMan):
        #self.currentAction = self.Move()
        #self.currentAction = map.BlockAction(self.currentAction, (self.x, self.y+1))
        self.SetPos(self.tileX, self.tileY - 1)

    def MoveDown(self):
        self.SetPos(self.tileX, self.tileY+1)
    def MoveLeft(self):
        self.SetPos(self.tileX-1, self.tileY)
    def MoveRight(self):
        self.SetPos(self.tileX+1, self.tileY)

