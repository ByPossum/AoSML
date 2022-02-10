import pygame
import sys
from MapManager import MapMan
from TilePainter import TileDrawing
from Player import Player
from consts import *

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
        pygame.display.flip()


    def Run(self):
        while self.Running:
            self.InputLoop()
            self.GameplayLoop()
            self.RenderLoop()

    def InputLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.Exit()
                elif event.key == pygame.K_w:
                    self.player.MoveUp(self.map)
                elif event.key == pygame.K_a:
                    self.player.MoveLeft()
                elif event.key == pygame.K_s:
                    self.player.MoveDown()
                elif event.key == pygame.K_d:
                    self.player.MoveRight()


    def RenderLoop(self):
        self.screen.fill(BACKGROUND_COLOUR)
        background = self.background.GetSurface()
        self.screen.blit(background, (background.get_rect().x, background.get_rect().y))
        player = self.player.sprite
        self.screen.blit(player.image, (player.rect.x, player.rect.y))
        pygame.display.flip()

    def GameplayLoop(self):
        self.player.Move()

    def Exit(self):
        self.Running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()
