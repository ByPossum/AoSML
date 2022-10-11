import pygame
import sys
from PlayerActions import PlayerAction
from MapManager import MapMan
from MapGeneration import LEGAL_MOVES
from TilePainter import TileDrawing
from Player import Player
from consts import *
import numpy

class GameLoop:

    def __init__(self):
        self.Running = True
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock
        pygame.display.set_caption("Ashes of Surtr: Machine Learning Edition")
        self.map = MapMan()
        self.background = TileDrawing(self.map.GetMap(), 800, 800)
        self.player = Player()
        startPos = self.map.GetStartPos()
        self.player.SetStartingPos(startPos[0], startPos[1])
        pygame.display.flip()


    def Run(self, sumo, model = None):
        while self.Running:
            if not sumo:
                self.InputLoop()
            elif sumo:
                self.RequestModelInput(model)
            self.GameplayLoop()
            self.RenderLoop()

    def InputLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.Exit()
                if self.player.GetMoving() != PlayerAction.none:
                    return
                elif event.key == pygame.K_w:
                    self.player.MoveUp(self.map)
                elif event.key == pygame.K_a:
                    self.player.MoveLeft(self.map)
                elif event.key == pygame.K_s:
                    self.player.MoveDown(self.map)
                elif event.key == pygame.K_d:
                    self.player.MoveRight(self.map)

    def RequestModelInput(self, model):
        if self.player.GetMoving() != PlayerAction.none:
            return None
        action = model.predict(self.GetMap().reshape((1, 1, self.map.map.width, self.map.map.height, 1)))
        index = numpy.argmax(action)
        self.TranslatePlayerMove(LEGAL_MOVES[index])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.Exit()

    def RenderLoop(self):
        self.screen.fill(BACKGROUND_COLOUR)
        background = self.background.GetSurface()
        self.screen.blit(background, (background.get_rect().x, background.get_rect().y))
        player = self.player.sprite
        self.screen.blit(player.image, (player.rect.x, player.rect.y))
        pygame.display.flip()

    def GameplayLoop(self):
        self.player.Update()

    def Exit(self):
        self.Running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def GetMap(self):
        return numpy.array(self.map.GetMapButMakeItNumbersWithPlayer((self.player.tileX, self.player.tileY))).reshape((self.map.map.width, self.map.map.height, 1))

    def CheckDone(self):
        return False

    def TranslatePlayerMove(self, action):
        if action == (-1, 0):
            self.player.MoveLeft(self.map)
        if action == (0, 1):
            self.player.MoveUp(self.map)
        if action == (1, 0):
            self.player.MoveRight(self.map)
        if action == (0, -1):
            self.player.MoveDown(self.map)

    def ResetBaybee(self):
        self.map = MapMan()
        startPos = self.map.GetStartPos()
        self.player.SetStartingPos(startPos[0], startPos[1])
        pygame.display.flip()

    def DebugMap(self):
        self.map.map.DebugMap()

    def DistanceToGoal(self):
        return self.map.map.GetDistanceToGoal((self.player.tileX, self.player.tileY))