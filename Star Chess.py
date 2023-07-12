"""
STAR CHESS BY ARMANDO CHAPARRO 10/07/23

THIS PROJECT STARTED 3 YEARS AGO WITH ALMOST NO KNOWLEDGE ABOUT PROGRAMMING,
I HAD A LITTLE BIT OF LOGIC BUT I WAS RECENTLY INTRODUCED TO PYTHON AND PYGAME.

I HOPE YOU LIKE IT.
"""

# MODULES
import pygame
from audio import mixer
from scripts import board
from scripts import intro

# PYGAME WINDOW
pygame.init()
# SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN = pygame.display.set_mode((960, 540))

# MAIN LOOP
if __name__ == '__main__':
    MIXER = mixer.Mixer(__file__)
    INTRO = intro.Intro(SCREEN, MIXER, __file__)
    BOARD = board.Board(SCREEN, MIXER, __file__)

    while True:
        INTRO.reset()
        BOARD.reset()
        if not INTRO.main(): break
        BOARD.connect(BOARD.ip, BOARD.port)
        BOARD.intro()