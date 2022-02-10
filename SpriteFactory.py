import pygame

class SpriteFactory(pygame.sprite.Sprite):

    def __init__(self, filepath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filepath)
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)

    def SetPos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def GetSpriteSurf(self):
        return self.image
    