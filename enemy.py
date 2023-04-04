import pygame
from pygame.sprite import Sprite
from random import randint


class Enemy(Sprite):
    """A class to represent an alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the enemy and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the enemy image and get its rect
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect()

        # Start each enemy randomly positioned on the screen
        self.rect.x = randint(64, self.settings.screen_dimensions[0] - 64)
        self.rect.y = randint(64, self.settings.screen_dimensions[1] - 64)

        # Choose random x and y direction
        self.x_direction = randint(0, 1)
        self.y_direction = randint(0, 1)
        if self.x_direction % 2 == 0:
            self.x_direction = -1
        if self.y_direction % 2 == 0:
            self.y_direction = -1

        # Store the enemy's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Change enemy direction if they touch the side"""
        # WILL NEED TO CHANGE THIS ONCE WE HAVE BLOCKS
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right - 32 or self.rect.left <= 32:
            self.x_direction *= -1

        if self.rect.bottom >= screen_rect.bottom - 32 or self.rect.top <= 32:
            self.y_direction *= -1

    def update(self):
        """Move the alien to the left or right"""
        self.check_edges()
        self.x += self.settings.enemy_speed * self.x_direction
        self.y += self.settings.enemy_speed * self.y_direction

        self.rect.x = self.x
        self.rect.y = self.y