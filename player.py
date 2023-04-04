import pygame
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, pac):
        super().__init__()

        self.screen = pac.screen
        self.screen_rect = pac.screen.get_rect()
        self.settings = pac.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('assets/player_still.png')
        self.rect = self.image.get_rect()

        # Start each new player at the top left of the screen.
        self.rect.topleft = self.screen_rect.topleft

        # Store a decimal value for the player's horizontal position.
        self.x = self.rect.x
        self.y = self.rect.y

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the player's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.player_speed
            self.rect.x = self.x
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.player_speed
            self.rect.x = self.x
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.player_speed
            self.rect.y = self.y
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.player_speed
            self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def _restart_player(self):
        self.moving_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.rect.topleft = self.screen_rect.topleft
        self.x = self.rect.x
        self.y = self.rect.y


    def round32(self, x):
        return (x + 16) & ~31

    def round_x(self):
        self.rect.x = self.round32(int(self.x))

    def round_y(self):
        self.rect.y = self.round32(int(self.y))