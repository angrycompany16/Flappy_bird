import pygame
from scripts.constants import *
from scripts.player import Player
from scripts.obstacle import Obstacle
from scripts.gamestats import GameStats, GameState

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

        self._objects = []
        self._objects.append(Obstacle())
        self._objects.append(self._player)

    def update(self) -> None:
        self._game_surf.fill(BLACK)
        dt = self._clock.tick() / 1000      # dt in seconds

        self._background_surf.fill(RED)
        match GameStats.current_state:
            case GameState.START_MENU:
                self._start_menu_surf.fill(pygame.Color(0, 0, 0, 0))
                self._start_menu_surf.blit(self._floor_image, (0, 0))
                self._background_surf.blit(self._background_image, (0, 0))



                self._game_surf.blit(self._background_surf, (0, 0))
                self._game_surf.blit(self._start_menu_surf, (0, 0))
            case GameState.PLAYING:
                GameStats.update_stats(dt)
                # self._background_surf.fill()
                self._playing_surf.fill(pygame.Color(0, 0, 0, 0))
                self._playing_surf.convert_alpha()
                self._background_surf.blit(self._background_image, (0, 0))
                self._playing_surf.blit(self._floor_image, (0, 0))

                for object in self._objects:
                    object.update(dt)
                    object.draw(self._playing_surf)

                self._game_surf.blit(self._background_surf, (0, 0))
                self._game_surf.blit(self._playing_surf, (0, 0))
            case GameState.GAME_OVER:
                self._game_over_surf.fill(pygame.Color(0, 0, 0, 0))
                self._background_surf.blit(self._background_image, (0, 0))
                self._playing_surf.fill(pygame.Color(0, 0, 0, 0))                
                self._playing_surf.blit(self._floor_image, (0, 0))

                GameStats.obstacle_movement_speed = 0

                for object in self._objects:
                    object.update(dt)
                    object.draw(self._playing_surf)

                self._game_surf.blit(self._background_surf, (0, 0))
                self._game_surf.blit(self._playing_surf, (0, 0))
                self._game_surf.blit(self._game_over_surf, (0, 0))
            case GameState.PAUSED:
                pass
            case _:
                print("Game state error")


        
    def handle_input(self, key) -> None:
        if key == pygame.K_UP or key == pygame.K_SPACE:
            if GameStats.current_state == GameState.START_MENU:
                GameStats.current_state = GameState.PLAYING
                self._player.jump()
            elif GameStats.current_state == GameState.PLAYING:
                self._player.jump()


    @property
    def game_surf(self) -> pygame.Surface:
        return self._game_surf
    

    