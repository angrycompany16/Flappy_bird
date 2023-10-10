from enum import Enum


class GameState(Enum):
    PLAYING = 0,
    GAME_OVER = 1,
    PAUSED = 2,
    START_MENU = 3

class GameStats():
    obstacle_movement_speed = 40
    obstacle_spacing = 100
    obstacle_spawn_period = 4

    current_state = GameState.START_MENU

    @classmethod
    def update_stats(cls, dt):
        cls.obstacle_movement_speed += 0.001 * dt
        cls.obstacle_spacing -= 0.001 * dt