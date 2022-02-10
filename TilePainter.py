import copy

import pygame
from SpriteFactory import SpriteFactory as sf

class TileDrawing:

    def __init__(self, map, width, height):
        pygame.init()
        self.map = map
        self.tileSet = {}
        self.LoadTileSet()
        self.surf = pygame.Surface((width, height))

        collectedMap = self.DrawMap()
        collectedMap.draw(self.surf)


    def LoadTileSet(self):
        floor = "Assets/floor.png"
        wall = "Assets/wall.png"
        pit = "Assets/pit.png"
        entrance = "Assets/entrance.png"
        exit = "Assets/exit.png"
        self.tileSet.update({'f': floor})
        self.tileSet.update({'w': wall})
        self.tileSet.update({'p': pit})
        self.tileSet.update({'s': entrance})
        self.tileSet.update({'e': exit})


    def DrawMap(self):
        mapSprites = pygame.sprite.Group()
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] in self.tileSet.keys():
                    newSprite = sf(self.tileSet[self.map[x][y]])
                    newSprite.SetPos(x*32, y*32)
                    mapSprites.add(newSprite)
        return mapSprites

    def GetSurface(self):
        return self.surf
