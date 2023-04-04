import pygame
from pygame.sprite import Sprite


class FilledBlock(Sprite):
    """Class for the already filled in blocks"""

    def __init__(self, pacXOR):
        super().__init__()
        self.screen = pacXOR.screen
        self.settings = pacXOR.settings

        # Load the image
        self.image = pygame.image.load('assets/filled_block.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height


class FollowingBlock(Sprite):
    """Class for the following blocks"""

    def __init__(self, pacXOR):
        super().__init__()
        self.screen = pacXOR.screen
        self.settings = pacXOR.settings

        # Load the image
        self.image = pygame.image.load('assets/filling_block.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def blitme(self, x, y):
        self.rect = (x, y)
        self.blitme(self.image, self.rect)

