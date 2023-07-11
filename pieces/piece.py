import os
import pygame
from scripts import functions
from scripts.resolution import ResolutionScreen

# BOARD MEASURES
SQUARE = 110
TOP = 95
LEFT = 520

# COLORS
RED = (217, 0, 8)
BLUE = (16, 115, 230)
GREEN = (66, 226, 154)
YELLOW = (204, 179, 97)

class Piece:
    def __init__(self, board, screen: pygame.Surface, path: str, image: str, x: int, y: int, team: str, name: str):

        # BOARD
        self.board = board

        # SCREEN PROPERTIES
        self.screen = ResolutionScreen(screen, 1920, 1080)

        # PIECE PROPERTIES
        self.team = team
        self.moved = False
        self.hovered = False
        self.selected = False
        self.x, self.y = x, y
        self.possible_moves: list[pygame.Vector2] = list()
        self.possible_moves_rects: list[pygame.Rect] = list()

        # FONT
        self.path = os.path.dirname(path)
        font_path = functions.resource_path(f'{self.path}/font/pixel.ttf')
        self.font = pygame.font.Font(font_path, int(self.screen.convert(48)))

        # NAME
        self.name = self.font.render(name, True, 'white')
        self.name_background = pygame.Surface(self.name.get_size())
        self.name_background.fill('black')
        self.name_background.set_alpha(127)
        self.get_name_rect()

        # IMAGE
        self.path = os.path.dirname(path)
        image_path = functions.resource_path(f'{self.path}/images/{image}.png')
        self.image = self.screen.load_image(image_path)

        # COLORS
        self.color = RED if team=='black' else BLUE
        self.hover_color = self.alpha_rect(YELLOW, 0.5)
        self.move_color = self.alpha_rect(self.color, 0.15)
        self.select_color = self.alpha_rect(self.color, 1)

        # RECT
        self.rect = self.get_rect(self.x, self.y)

        # ANIMATION
        self.select_anim = functions.DeltaValue(
            duration=2000, min_value=127, max_value=255,
            function=self.select_color.set_alpha
        )

        # FLAGS
        self.flag = None

    def check_flag(self) -> None:
        if not self.flag: return
        self.flag = self.flag()
    
    def update_next_turn(self, variable: str, value: object) -> None:
        self.flag = lambda: setattr(self, variable, value)

    def get_name_rect(self) -> None:
        centerx = self.screen.convert(((self.x+0.5)*SQUARE + LEFT))
        bottom = self.screen.convert((self.y*SQUARE + TOP - 5))
        self.name_rect = self.name.get_rect(bottom=bottom, centerx=centerx)

    def update(self, dt: int) -> None:
        if self.selected: self.select_anim.update(dt)

    def collide(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def is_enemy(self, pos: tuple[int, int]) -> bool:
        if not (piece := self.board.get(pos)): return False
        return piece.team != self.team

    def get_rect(self, x: int, y: int) -> pygame.Rect:
        return self.screen.get_rect(self.image, ((x*SQUARE+LEFT), (y*SQUARE+TOP)))

    def move(self, pos: tuple[int, int], change_turn: bool=True) -> None:
        self.board.move((self.x, self.y), pos, change_turn)
        self.x, self.y = pos
        self.get_name_rect()
        self.rect = self.get_rect(self.x, self.y)
        self.selected = False
        if not self.moved: self.moved = True

        # PLAY MOVE SOUND
        self.board.mixer.play_sound('move.wav')

    def click(self, event: pygame.event) -> None:
        self.selected = self.collide(event.pos)
        return self.selected
    
    def hover(self, event: pygame.event) -> None:
        self.hovered = self.collide(event.pos)

    def show(self) -> None:
        if self.selected: self.screen.blit(self.select_color, self.rect)
        elif self.hovered: self.screen.blit(self.hover_color, self.rect)
        self.screen.blit(self.image, self.rect)
        
    def show_name(self) -> None:
        if not self.hovered: return
        self.screen.blit(self.name_background, self.name_rect)
        self.screen.blit(self.name, self.name_rect)
    
    def show_moves(self) -> None:
        if not self.selected: return
        if not self.possible_moves: return
        for rect in self.possible_moves_rects:
            self.screen.blit(self.move_color, rect)

    def alpha_rect(self, color: str|tuple[int, int, int], alpha: float) -> pygame.Surface:
        surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        surface.set_alpha(int(255*alpha))
        surface.fill(color)
        return surface

    def calculate_moves_rects(self) -> None:
        self.possible_moves_rects.clear()
        self.possible_moves_rects = [
            self.get_rect(*move)
            for move in self.possible_moves
        ]
    
    def available(self, pos: tuple[int, int]) -> bool:
        return self.board.available(pos)

    def check_moves(self, moves: list[tuple[int, int]]) -> None:
        for move in moves:
            if self.available(move): self.possible_moves.append(move)
            elif self.is_enemy(move): return self.possible_moves.append(move)
            else: return
    
    def in_attack(self, pos: tuple[int, int]) -> bool:
        return self.board.in_attack(pos)

