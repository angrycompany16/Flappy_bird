from enum import Enum


class GameState(Enum):
    PLAYING = 0,
    GAME_OVER = 1,
    PAUSED = 2,
    START_MENU = 3

class GameStats():
    obstacle_movement_speed = 40
    obstacle_spacing = 100
    obstacle_spawn_period = 2

    current_state = GameState.START_MENU
    points = 0

    @classmethod
    def update_stats(cls, dt):
        cls.obstacle_movement_speed += 0.01 * dt
        cls.obstacle_spacing -= 0.1 * dt
        cls.obstacle_spawn_period -= 0.01 * dt