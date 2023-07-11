import pygame
from scripts import board
from scripts import intro
from audio import mixer

# PYGAME WINDOW
pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# MAIN LOOP
if __name__ == '__main__':
    while True:
        MIXER = mixer.Mixer(__file__)
        INTRO = intro.Intro(SCREEN, MIXER, __file__)
        if not INTRO.main(): break

        BOARD = board.Board(SCREEN, MIXER, __file__)
        BOARD.intro()