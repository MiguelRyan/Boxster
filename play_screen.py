import pygame.font
from button import Button


class PlayScreen:
    """A class to report scoring information"""

    def __init__(self, pac):
        """Initialize scorekeeping attributes."""
        self.pac = pac
        self.screen = pac.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pac.settings
        # self.stats = pac.stats

        # Font settings for scoring information
        self.text_colour = self.settings.title_label_colour
        self.title_font = pygame.font.SysFont("impact", 180)
        self.description_font = pygame.font.SysFont("impact", 24)

    def show_title(self):
        """Turn the score into a rendered image"""
        title_str = self.settings.game_name
        description_str = self.settings.description

        self.title_image = self.title_font.render(title_str, True, self.text_colour, self.settings.background_colour)
        self.description_image = self.description_font.render(
            description_str, True, self.text_colour, self.settings.background_colour)

        # Display the score at the top right of the screen.
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = self.screen_rect.top + 128

        self.description_rect  =self.description_image.get_rect()
        self.description_rect.centerx = self.screen_rect.centerx
        self.description_rect.top = self.title_rect.bottom - 20

        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.description_image, self.description_rect)

    def create_play_button(self):
        play_button = Button(
            self, "Play",
            self.screen_rect.centerx, self.description_rect.bottom + 64, 100, 60,
            (255, 255, 255), (60, 255, 60)
        )

        play_button.draw_button()
        self.play_button = play_button

    def load(self):
        self.screen.fill(self.settings.background_colour)
        self.show_title()
        self.create_play_button()
