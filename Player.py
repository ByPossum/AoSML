from SpriteFactory import SpriteFactory
from MapManager import MapMan
from PlayerActions import PlayerAction
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
        self.startX = 0
        self.startY = 0
        self.currentAction = PlayerAction.none
        self.moveCheck = False

    def SetPos(self, x, y):
        self.tileX = x
        self.tileY = y
        self.SetTarget(self.tileX, self.tileY)

    def SetTarget(self, x, y):
        self.targetX = x * 32
        self.targetY = y * 32

    def SetStartingPos(self, x, y):
        self.SetPos(x, y)
        self.startX = x
        self.startY = y
        self.x = self.targetX
        self.y = self.targetY
        self.UpdateRect()

    def UpdateRect(self):
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y

    def Update(self):
        if self.currentAction == PlayerAction.move:
            self.Move()
        if self.currentAction == PlayerAction.pit:
            self.FallInPit()


    def Move(self):
        if self.x < self.targetX:
            self.x += MOVESPEED
        elif self.x > self.targetX:
            self.x -= MOVESPEED
        if self.y < self.targetY:
            self.y += MOVESPEED
        elif self.y > self.targetY:
            self.y -= MOVESPEED
        self.currentAction = PlayerAction.none if self.x == self.targetX and self.y == self.targetY else self.currentAction
        self.UpdateRect()

    def FallInPit(self):
        self.SetStartingPos(self.startX, self.startY)
        print("Fell into a pit")
        self.currentAction = PlayerAction.none
        pass

    def MoveUp(self, map: MapMan):
        self.currentAction = self.GetActionBasedOnMovement(self.tileX, self.tileY - 1, map)
    def MoveDown(self, map: MapMan):
        self.currentAction = self.GetActionBasedOnMovement(self.tileX, self.tileY+1, map)
    def MoveLeft(self, map: MapMan):
        self.currentAction = self.GetActionBasedOnMovement(self.tileX-1, self.tileY, map)
    def MoveRight(self, map: MapMan):
        self.currentAction = self.GetActionBasedOnMovement(self.tileX+1, self.tileY, map)

    def GetActionBasedOnMovement(self, x, y, map: MapMan):
        if self.currentAction == PlayerAction.none:
            self.currentAction = map.CheckNextBlock((x, y))
            if self.currentAction == PlayerAction.move:
                self.SetPos(x, y)
                return PlayerAction.move
            if self.currentAction == PlayerAction.pit:
                return PlayerAction.pit
            return PlayerAction.none
