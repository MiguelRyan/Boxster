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
        self.filled_block_location_list=[]
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
                    self.enemy_hit_barrier_block()
                    for enemy in self.enemies:
                        enemy.update()
            else:
                self.player.update()
                self.playscreen.load()
                self.barrier.draw(self.screen)
                self.player.blitme()
                self.play_button_pressed()

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

        if event.key == pygame.K_p:
            self.GAME_PAUSED = not self.GAME_PAUSED

        if event.key == pygame.K_e:
            self.spawn_enemy()
            self.spawn_enemy()

        if event.key == pygame.K_f:
            self.fill_empty_areas()

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
            self._create_following_block(grid_location[0] * 32, grid_location[1] * 32)

    def _check_following_to_barrier(self):
        # Collision between player and non-following block
        collisions = pygame.sprite.spritecollide(self.player, self.barrier, False)

        if collisions and self.following_block_location_list:
            self.following_block_location_list = []
            for following_block in self.following_blocks:
                x = following_block.rect.x
                y = following_block.rect.y
                self._create_block(x, y)
                self.filled_block_location_list.append(self._convert_pixel_to_grid(x, y))
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

    def enemy_hit_barrier_block(self):
        collisions = pygame.sprite.groupcollide(self.enemies, self.barrier, False, False)

        for enemy in collisions:
            block = collisions[enemy][0]
            if enemy.rect.right - 1 == block.rect.left or enemy.rect.left + 1 == block.rect.right:
                enemy.x_direction *= -1

            if enemy.rect.top + 1 == block.rect.bottom or enemy.rect.bottom - 1 == block.rect.top:
                enemy.y_direction *= -1

    def play_button_pressed(self):
        collisions = pygame.sprite.collide_rect(self.player, self.playscreen.play_button)
        if collisions:
            self.GAME_STARTED = True
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


    def fill_empty_areas(self):
        no_block_grid = []

        # Find all grid spaces that don't contain blocks already and add to list no_block_grid
        width, height = self._convert_pixel_to_grid(self.screen.get_width(), self.screen.get_height())
        for y in range(1, height-1):
            for x in range(1, width-1):
                if [x, y] not in self.following_block_location_list and [x, y] not in self.filled_block_location_list:
                    no_block_grid.append([x, y])

        for x,y in no_block_grid:
            grid = self._convert_grid_to_pixel(x,y)
            self._create_block(grid[0], grid[1])

    def quit_game(self):
        """Quits the game"""
        sys.exit()


if __name__ == "__main__":
    game = Boxster()
