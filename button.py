import pygame

class Button:
    """Class for a button takes args: text, x, y, width, length"""
    def __init__(self, pac, text, x, y, width, height, text_colour, button_colour):
        self.pac = pac
        self.screen = self.pac.screen
        self.screen_rect = self.screen.get_rect()

        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_colour = text_colour
        self.button_colour = button_colour

        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.msg_image = self.font.render(self.text, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _check_player_collision(self):
        collisions = pygame.sprite.spritecollide(self.pac.player, self.rect, False)

