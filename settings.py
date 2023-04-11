class Settings:

    def __init__(self):
        self.screen_dimensions = (1184, 640)
        self.background_colour = (255, 255, 153)

        # Player settings
        self.player_speed = 0.65

        # Enemy settings
        self.enemy_speed = 0.15

        # Play screen settings
        self.game_name = "Boxster"
        self.title_label_colour = (153, 204, 255)
        self.description = "Fill up most of the screen with boxes while avoiding enemies, " \
                           "Use the character to start the game."