import pygame.font
from pygame.sprite import Group

class HUD:
    """A class to report scoring information"""

    def __init__(self, pac):
        """Initialize scorekeeping attributes."""
        self.pac = pac
        self.screen = pac.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pac.settings
        #self.stats = pac.stats

        # Font settings for scoring information
        self.text_colour = (30, 30, 30)
        self.score_font = pygame.font.SysFont(None, 48)
        self.game_over_font = pygame.font.SysFont("impact", 160)

        # Prepare the initial score image.
        self.prep_score()

    def prep_score(self):
        """Turn the score into a rendered image"""
        percent_filled = (len(self.pac.barrier) - 114) / 630
        score_str = "Percent: " + str(percent_filled * 100)[:4] + "%"
        self.score_image = self.score_font.render(score_str, True, self.text_colour, (255, 162, 63))

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 32
        self.score_rect.top = 0

    def show_score(self):
        """Draw scores, ships and levels to the screen"""
        self.screen.blit(self.score_image, self.score_rect)

    def show_game_over(self):
        self.game_over_image = self.game_over_font.render("Game Over", True, (248, 58, 58), self.settings.background_colour)
        self.game_over_rect = self.game_over_image.get_rect()

        self.game_over_rect.top = 64
        self.game_over_rect.centerx = self.screen_rect.centerx

        self.screen.blit(self.game_over_image, self.game_over_rect)
