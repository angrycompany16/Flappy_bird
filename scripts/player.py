import pygame
from scripts.constants import *
from scripts.object import Object
from scripts.collision_checker import CollisionChecker
from scripts.gamestats import GameStats, GameState
from scripts.sound_manager import SoundManager

class Player(Object):
    def __init__(self) -> None:
        self._flap_up_image = pygame.image.load("images/player-flap-up.png")
        self._flap_down_image = pygame.image.load("images/player-flap-down.png")
        self._image = self._flap_up_image
        self._rect = self._image.get_rect()
        self._position = pygame.Vector2(PLAYER_LEFT_POS / SUBPIXEL_SCALE_FACTOR, (GAME_HEIGHT - self._rect.height) / (SUBPIXEL_SCALE_FACTOR * 2))
        self._velocity = pygame.Vector2(0, 0)
        self._acceleration = pygame.Vector2(0, GRAVITY)
        self._rotation = 0
        self._has_crashed_with_ground = False
        self._has_crashed_with_obstacle = False

        self._rect.topleft = self._position
        
        CollisionChecker.add_collider(self._rect)

    def update(self, dt) -> None:
        self._velocity += self._acceleration * dt
        self._position += self._velocity * dt

        if self._position.y > (GAME_HEIGHT - FLOOR_HEIGHT - self._rect.height) / SUBPIXEL_SCALE_FACTOR:
            self._position.y = (GAME_HEIGHT - FLOOR_HEIGHT - self._rect.height) / SUBPIXEL_SCALE_FACTOR
            self._velocity.y = 0
            GameStats.current_state = GameState.GAME_OVER

            if not self._has_crashed_with_ground:
                SoundManager.slap_sound.play()
                self._has_crashed_with_ground = True

        self._rect.topleft = self._position * SUBPIXEL_SCALE_FACTOR

        if CollisionChecker.check_collisions(self._rect):
            GameStats.current_state = GameState.GAME_OVER

            if not self._has_crashed_with_obstacle:
                SoundManager.bonk_sound.play()
                self._has_crashed_with_obstacle = True


    def draw(self, game_surf) -> None:
        if GameStats.current_state != GameState.GAME_OVER:
            self._rotation = -self._velocity.y

        rotated_image = pygame.transform.rotate(self._image, self._rotation)
        img_center = self._image.get_rect(topleft=self._rect.topleft).center
        new_rect = rotated_image.get_rect(center=img_center)

        self._image.convert_alpha()
        game_surf.blit(rotated_image, new_rect)
        # pygame.draw.rect(game_surf, RED, self._rect, 1)

    def jump(self) -> None:
        self._velocity = pygame.Vector2(self._velocity.x, -JUMP_SPEED)

    def flap_down(self) -> None:
        self._image = self._flap_down_image

    def flap_up(self) -> None:
        self._image = self._flap_up_image