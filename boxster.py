import sys
import time

import pygame
from settings import Settings
from player import Player
from enemy import Enemy
from blocks import FilledBlock, FollowingBlock
from HUD import HUD
from play_screen import PlayScreen


class Boxster:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_dimensions)
        pygame.display.set_caption(self.settings.game_name)
        self.GAME_STARTED = False
        self.GAME_PAUSED = False

        self.playscreen = PlayScreen(self)
        self.player = Player(self)

        self.enemies = pygame.sprite.Group()
        self.barrier = pygame.sprite.Group()
        self.following_blocks = pygame.sprite.Group()
        self.following_block_location_list = []
        self._create_barrier()

        self.HUD = HUD(self)

        self.run_game()

    def run_game(self):
        """Main loop for the game"""
        while True:
            self._check_key_presses()
            if self.GAME_STARTED:
                self._update_screen()
                if not self.GAME_PAUSED:
                    self.player.update()
                    self.create_following_block()
                    self._check_following_to_barrier()
                    self._detect_enemy_following_block()
                    for enemy in self.enemies:
                        enemy.update()
            else:
                self.player.update()
                self.playscreen.load()
                self.barrier.draw(self.screen)
                self.player.blitme()

            pygame.display.flip()

    def _update_screen(self):
        """Updated every frame"""
        self.screen.fill(self.settings.background_colour)
        self.enemies.draw(self.screen)
        self.barrier.draw(self.screen)
        self.following_blocks.draw(self.screen)
        self.player.blitme()
        self.HUD.show_score()


    def _check_key_presses(self):
        """Checks if anything is pressed"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            if event.type == pygame.KEYDOWN:
                self._down_key_press(event)

    def _down_key_press(self, event):
        """When a key is pressed check what to do"""
        if event.key == pygame.K_ESCAPE:
            self.quit_game()

        if event.key == pygame.K_RIGHT:
            self.player.moving_left = False
            self.player.moving_right = True
            self.player.moving_down = False
            self.player.moving_up = False
            self.player.round_y()

        if event.key == pygame.K_LEFT:
            self.player.moving_left = True
            self.player.moving_right = False
            self.player.moving_down = False
            self.player.moving_up = False
            self.player.round_y()

        if event.key == pygame.K_DOWN:
            self.player.moving_left = False
            self.player.moving_right = False
            self.player.moving_down = True
            self.player.moving_up = False
            self.player.round_x()

        if event.key == pygame.K_UP:
            self.player.moving_left = False
            self.player.moving_right = False
            self.player.moving_down = False
            self.player.moving_up = True
            self.player.round_x()

        if event.key == pygame.K_f:
            self.GAME_STARTED = True
            self._game_restart()

        if event.key == pygame.K_p:
            self.GAME_PAUSED = not self.GAME_PAUSED

        if event.key == pygame.K_e:
            self.spawn_enemy()
            self.spawn_enemy()

    def _create_block(self, x, y):
        block = FilledBlock(self)
        block.x = x
        block.y = y
        block.rect.x = block.x
        block.rect.y = block.y

        self.barrier.add(block)

    def _create_following_block(self, x, y):
        block = FollowingBlock(self)
        block.x = x
        block.y = y
        block.rect.x = block.x
        block.rect.y = block.y

        self.following_blocks.add(block)

    def _create_barrier(self):
        for block in range(0, int(self.settings.screen_dimensions[0] / 32)):
            self._create_block(block * 32, 0)
            self._create_block(block * 32, self.settings.screen_dimensions[1] - 32)

        for block in range(0, int(self.settings.screen_dimensions[1] / 32)):
            self._create_block(0, block * 32)
            self._create_block(self.settings.screen_dimensions[0] - 32, block * 32)

    def spawn_enemy(self):
        """Spawns an enemy and adds it to the group enemies"""
        enemy = Enemy(self)
        self.enemies.add(enemy)

    def create_following_block(self):
        collisions = pygame.sprite.spritecollide(self.player, self.barrier, False)
        grid_location = self._convert_pixel_to_grid(self.player.rect.x, self.player.rect.y)
        if not collisions and grid_location not in self.following_block_location_list:
            self.following_block_location_list.append(grid_location)
            self._create_following_block(grid_location[0]*32, grid_location[1]*32)

    def _check_following_to_barrier(self):
        collisions = pygame.sprite.spritecollide(self.player, self.barrier, False)

        if collisions and self.following_block_location_list:
            self.following_block_location_list = []
            for following_block in self.following_blocks:
                self._create_block(following_block.rect.x, following_block.rect.y)
            self.following_blocks.empty()
            self.HUD.prep_score()

    def _convert_pixel_to_grid(self, x, y):
        """Simple function that given pixel location will output which gridbox that pixel is in"""
        self.gridbox_x = ((x + 16) & ~31) / 32
        self.gridbox_y = ((y + 16) & ~31) / 32

        return [int(self.gridbox_x), int(self.gridbox_y)]

    def _convert_grid_to_pixel(self, x, y):
        """Function that does the opposite conversion of _convert_pixel_to_grid"""
        self.pixel_x = x * 32
        self.pixel_y = y * 32

        return [int(self.pixel_x), int(self.pixel_y)]

    def _detect_enemy_following_block(self):
        collisions = pygame.sprite.groupcollide(self.following_blocks, self.enemies, False, False)

        if collisions:
            self.HUD.show_game_over()
            self._game_restart()

    def _detect_player_following_block_detection(self):
        print(len(self.following_block_location_list), len(self.following_blocks))

    def _game_restart(self):
        self.enemies.empty()
        self.barrier.empty()
        self.following_blocks.empty()
        self.following_block_location_list = []
        self._create_barrier()
        self.player._restart_player()

    def quit_game(self):
        """Quits the game"""
        sys.exit()


if __name__ == "__main__":
    game = Boxster()
