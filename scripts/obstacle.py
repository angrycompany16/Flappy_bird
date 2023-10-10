import pygame
from scripts.object import Object
from scripts.constants import *
from scripts.gamestats import GameStats
from scripts.collision_checker import CollisionChecker
from random import uniform

class Obstacle(Object):
    def __init__(self) -> None:
        self._top = pygame.image.load("images/pipe-top.png")
        self._bottom = pygame.image.load("images/pipe-bottom.png")
        
        self._top_rect = self._top.get_rect()
        self._bottom_rect = self._bottom.get_rect()

        random_offset = GAME_HEIGHT - 32 - GameStats.obstacle_spacing
        # random_offset = uniform(32, GAME_HEIGHT - 32 - GameStats.obstacle_spacing)
        self._position = pygame.Vector2(GAME_WIDTH + self._top.get_width(), GAME_HEIGHT - random_offset)

        self._bottom_rect.topleft = self._position
        self._top_rect.topleft = (self._position.x, self._position.y - GameStats.obstacle_spacing - self._top.get_height())

        CollisionChecker.add_collider(self._top_rect)
        CollisionChecker.add_collider(self._bottom_rect)

    def update(self, dt) -> None:
        self._position.x -= GameStats.obstacle_movement_speed * dt
        self._bottom_rect.topleft = self._position
        self._top_rect.topleft = (self._position.x, self._position.y - GameStats.obstacle_spacing - self._top.get_height())

    def draw(self, game_surf) -> None:
        game_surf.blit(self._bottom, self._bottom_rect.topleft)
        game_surf.blit(self._top, self._top_rect.topleft)

        # pygame.draw.rect(game_surf, RED, self._top_rect, 1)
        # pygame.draw.rect(game_surf, RED, self._bottom_rect, 1)
