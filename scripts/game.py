import pygame
from scripts.constants import *
from scripts.player import Player
from scripts.obstacle import Obstacle
from scripts.gamestats import GameStats, GameState
from scripts.sound_manager import SoundManager
from scripts.collision_checker import CollisionChecker

class Game:
    def __init__(self) -> None:
        # solid surfaces
        self._game_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self._background_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        # overlay surfaces
        self._playing_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), flags=pygame.SRCALPHA)
        self._game_over_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), flags=pygame.SRCALPHA)
        self._paused_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), flags=pygame.SRCALPHA)
        self._start_menu_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), flags=pygame.SRCALPHA)

        self._player = Player()

        self._clock = pygame.time.Clock()

        self._background_image = pygame.image.load("images/background.png")
        self._floor_image = pygame.image.load("images/floor.png")
        self._floor_scroll = 0

        self._time_since_obstacle_spawn = 0
        self._time_since_death = 0

        self._font_big = pygame.font.Font("font/minecrafter/Minecrafter.Reg.ttf", size=18)
        self._font_small = pygame.font.Font("font/minecrafter/Minecrafter.Reg.ttf", size=12)

        self._objects = []
        self._objects.append(Obstacle())
        self._objects.append(self._player)

    def update(self) -> None:
        self._game_surf.fill(BLACK)
        dt = self._clock.tick() / 1000      # dt in seconds

        self._floor_scroll -= GameStats.obstacle_movement_speed * dt
        if self._floor_scroll < -self._floor_image.get_width():
            self._floor_scroll = 0
        
        self._background_surf.fill(RED)
        match GameStats.current_state:
            case GameState.START_MENU:
                self._start_menu_surf.fill(pygame.Color(0, 0, 0, 0))
                self._start_menu_surf.blit(self._floor_image, (round(self._floor_scroll), 0))
                self._start_menu_surf.blit(self._floor_image, (round(self._floor_scroll) + self._floor_image.get_width(), 0))
                self._background_surf.blit(self._background_image, (0, 0))

                self._game_surf.blit(self._background_surf, (0, 0))
                self._game_surf.blit(self._start_menu_surf, (0, 0))
            case GameState.PLAYING:
                GameStats.update_stats(dt)
                # self._background_surf.fill()
                self._playing_surf.fill(pygame.Color(0, 0, 0, 0))
                self._playing_surf.convert_alpha()
                self._background_surf.blit(self._background_image, (0, 0))

                self._time_since_obstacle_spawn += dt
                if self._time_since_obstacle_spawn > GameStats.obstacle_spawn_period:
                    self._time_since_obstacle_spawn = 0
                    self.spawn_obstacle()

                for object in self._objects:
                    object.update(dt)
                    object.draw(self._playing_surf)

                self._playing_surf.blit(self._floor_image, (round(self._floor_scroll), 0))
                self._playing_surf.blit(self._floor_image, (round(self._floor_scroll) + self._floor_image.get_width(), 0))

                text_surf = self._font_big.render(f"{GameStats.points}", False, WHITE).convert_alpha()
                outlined_text_surf = self.add_outline(text_surf, 1, (0, 0, 0))
                
                self._playing_surf.blit(outlined_text_surf, (GAME_WIDTH / 2 - outlined_text_surf.get_width() / 2, SCORE_Y_POS))
                self._game_surf.blit(self._background_surf, (0, 0))
                self._game_surf.blit(self._playing_surf, (0, 0))
            case GameState.GAME_OVER:
                self._game_over_surf.fill(pygame.Color(0, 0, 0, 0))
                self._background_surf.blit(self._background_image, (0, 0))
                self._playing_surf.fill(pygame.Color(0, 0, 0, 0))                

                GameStats.obstacle_movement_speed = 0
                self._time_since_death += dt

                for object in self._objects:
                    object.update(dt)
                    object.draw(self._playing_surf)

                self._playing_surf.blit(self._floor_image, (round(self._floor_scroll), 0))
                self._playing_surf.blit(self._floor_image, (round(self._floor_scroll) + self._floor_image.get_width(), 0))
                
                game_over_text = self._font_big.render("Game Over!", False, WHITE)
                game_over_text = self.add_outline(game_over_text, 1, (0, 0, 0))
                score_text = self._font_small.render(f"Final score: {GameStats.points}", False, WHITE)
                score_text = self.add_outline(score_text, 1, (0, 0, 0))
                # restart_text = self._font_small.render("Press Space to restart", False, WHITE)

                self._playing_surf.blit(game_over_text, (GAME_WIDTH / 2 -  game_over_text.get_width() / 2, 50))
                self._playing_surf.blit(score_text, (GAME_WIDTH / 2 - score_text.get_width() / 2, 80))
                self._game_surf.blit(self._background_surf, (0, 0))
                self._game_surf.blit(self._playing_surf, (0, 0))
                self._game_surf.blit(self._game_over_surf, (0, 0))
            case GameState.PAUSED:
                pass
                # Never got around to implementing this lol
            case _:
                print("Game state error")

    def handle_keypress(self, key) -> None:
        if key == pygame.K_UP or key == pygame.K_SPACE:
            if GameStats.current_state == GameState.START_MENU:
                GameStats.current_state = GameState.PLAYING
            elif GameStats.current_state == GameState.GAME_OVER:
                print(self._time_since_death)
                if self._time_since_death > 1:
                    self.restart()
                    GameStats.current_state = GameState.START_MENU

                return

            self._player.jump()
            self._player.flap_down()
            SoundManager.flap_sound.play()

    def handle_keyrelease(self, key) -> None:
        if key == pygame.K_UP or key == pygame.K_SPACE:
            self._player.flap_up()

    def spawn_obstacle(self) -> None:
        newObstacle = Obstacle()
        self._objects.insert(0, newObstacle)

    def restart(self) -> None:
        self._time_since_obstacle_spawn = 0
        self._time_since_death = 0
        
        CollisionChecker.clear_colliders()

        self._player = Player()

        self._objects = []
        self._objects.append(Obstacle())
        self._objects.append(self._player)
        GameStats.obstacle_movement_speed = 40
        GameStats.obstacle_spacing = 100
        GameStats.obstacle_spawn_period = 2

        GameStats.points = 0

    def add_outline(self, image, thickness, color, colorkey=pygame.Color(255, 0, 255)) -> pygame.surface:
        mask = pygame.mask.from_surface(image)
        mask_surf = mask.to_surface(setcolor=color, unsetcolor=RED)
        mask_surf.set_colorkey(RED)

        new_img = pygame.Surface((image.get_width() + thickness * 2, image.get_height() + thickness * 2))
        new_img.fill(colorkey)
        new_img.set_colorkey(colorkey)

        for i in -thickness, thickness:
            new_img.blit(mask_surf, (i + thickness, thickness))
            new_img.blit(mask_surf, (thickness, i + thickness))

        new_img.blit(image, (thickness, thickness))

        return new_img

    @property
    def game_surf(self) -> pygame.Surface:
        return self._game_surf
    

    