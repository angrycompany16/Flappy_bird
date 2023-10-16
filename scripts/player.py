import pygame
from scripts.constants import *
from scripts.object import Object
from scripts.collision_checker import CollisionChecker
from scripts.gamestats import GameStats, GameState

class Player(Object):
    def __init__(self) -> None:
        self._image = pygame.image.load("images/player.png")
        self._rect = self._image.get_rect()
        self._position = pygame.Vector2(PLAYER_LEFT_POS / SUBPIXEL_SCALE_FACTOR, (GAME_HEIGHT - self._rect.height) / (SUBPIXEL_SCALE_FACTOR * 2))
        self._velocity = pygame.Vector2(0, 0)
        self._acceleration = pygame.Vector2(0, GRAVITY)

        self._rect.topleft = self._position
        
        CollisionChecker.add_collider(self._rect)

    def update(self, dt) -> None:
        self._velocity += self._acceleration * dt
        self._position += self._velocity * dt

        if self._position.y > (GAME_HEIGHT - FLOOR_HEIGHT - self._rect.height) / SUBPIXEL_SCALE_FACTOR:
            self._position.y = (GAME_HEIGHT - FLOOR_HEIGHT - self._rect.height) / SUBPIXEL_SCALE_FACTOR
            self._velocity.y = 0
            GameStats.current_state = GameState.GAME_OVER

        self._rect.topleft = self._position * SUBPIXEL_SCALE_FACTOR

        if CollisionChecker.check_collisions(self._rect):
            GameStats.current_state = GameState.GAME_OVER

    def draw(self, game_surf) -> None:
        img_center = self._image.get_rect().center
        rotated_image = pygame.transform.rotate(self._image, self._velocity)
        new_rect = rotated_image.get_rect(center=image)

        self._image.convert_alpha()
        game_surf.blit(self._image, self._rect.topleft)
        pygame.draw.rect(game_surf, RED, self._rect, 1)

    def jump(self) -> None:
        self._velocity = pygame.Vector2(self._velocity.x, -JUMP_SPEED)