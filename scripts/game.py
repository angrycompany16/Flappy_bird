import pygame
from scripts.constants import *

class Game:
    def __init__(self) -> None:
        self._screen_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

    def update(self) -> None:
        self._screen_surf.fill(GREEN)
        self._screen_surf.convert()

    @property
    def screen_surf(self) -> pygame.Surface:
        return self._screen_surf