import pygame

pygame.mixer.init()

class SoundManager():
    slap_sound = pygame.mixer.Sound("sounds/Edited/slap.mp3")
    flap_sound = pygame.mixer.Sound("sounds/Edited/flap.mp3")
    bonk_sound = pygame.mixer.Sound("sounds/Edited/bonk.mp3")
    ding_sound = pygame.mixer.Sound("sounds/Raw/ding.wav")
