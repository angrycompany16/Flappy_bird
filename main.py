import pygame
from scripts.constants import *
from scripts.game import Game

SCREEN_WIDTH, SCREEN_HEIGHT = GAME_WIDTH * PIXEL_SCALE_FACTOR, GAME_HEIGHT * PIXEL_SCALE_FACTOR

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy!")

    game = Game()

    running = True
    while running:
        screen.fill(RED)

        game.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_keypress(event.key)
            elif event.type == pygame.KEYUP:
                game.handle_keyrelease(event.key)

        screen.blit(pygame.transform.scale(game.game_surf, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()