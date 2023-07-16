"""This script is just to compile the game to exe"""

import os

os.system('pyinstaller --noconfirm --onefile --windowed --add-data\
          "C:/Users/Lenovo/Python/Games/Star Chess/audio;audio/"\
          --add-data "C:/Users/Lenovo/Python/Games/Star Chess/font;font/"\
          --add-data "C:/Users/Lenovo/Python/Games/Star Chess/images;images/"\
          --add-data "C:/Users/Lenovo/Python/Games/Star Chess/pieces;pieces/"\
          --add-data "C:/Users/Lenovo/Python/Games/Star Chess/scripts;scripts/"\
          --add-data "C:/Users/Lenovo/Python/Games/Star Chess/settings;settings/" \
          --add-data "C:/Users/Lenovo/Python/Games/Star Chess/web;web/" \
          "C:/Users/Lenovo/Python/Games/Star Chess/Star Chess.py"')