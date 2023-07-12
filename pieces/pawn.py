import pygame
from pieces.piece import Piece


class Pawn(Piece):
    """Class Pawn"""
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):
        
        # GET IMAGE BASED ON STARTING POSITION
        image = 'rebel' if team == 'white' else 'death trooper'
        super().__init__(board, screen, path, image, x, y, team, 'PEON')

        # PAWN PROPERTIES
        self.dir = -1 if team == 'white' else 1
        self.en_passant_row = 3 if team == 'white' else 4
        self.double_move = (self.x, self.y+2*self.dir)
        self.double_move_rect = self.get_rect(*self.double_move)
        self.moved_twice = False
        self.can_passant = False

        self.left_passant = (self.x-1, self.en_passant_row)
        self.right_passant = (self.x+1, self.en_passant_row)
        self.left_passant_end = (self.x-1, self.en_passant_row+self.dir)
        self.right_passant_end = (self.x+1, self.en_passant_row+self.dir)
        self.left_passant_rect = self.get_rect(*self.left_passant_end)
        self.right_passant_rect = self.get_rect(*self.right_passant_end)
        self.can_left_passant = False
        self.can_right_passant = False
        self.allow_left_passant = True
        self.allow_right_passant = True
    
    def calculate_moves(self) -> None:
        """Updates the list of possible moves"""
        self.possible_moves.clear()

        # FRONT
        if self.board.available((self.x, self.y+self.dir)):
            self.possible_moves.append((self.x, self.y + self.dir))
            if (not self.moved) and (self.board.available((self.x, self.y+2*self.dir))):
                self.possible_moves.append((self.x, self.y+2*self.dir))

        # LEFT
        left = (self.x-1, self.y+self.dir)
        if self.is_enemy(left): self.possible_moves.append(left)

        # RIGHT
        right = (self.x+1, self.y+self.dir)
        if self.is_enemy(right): self.possible_moves.append(right)

        # EN PASSANT
        if self.y != self.en_passant_row: return
        left_passant = self.board.get(self.left_passant)
        if left_passant and left_passant.moved_twice and self.allow_left_passant:
            self.possible_moves.append(self.left_passant_end)
            self.can_left_passant = True

        right_passant = self.board.get(self.right_passant)
        if right_passant and right_passant.moved_twice and self.allow_right_passant:
            self.possible_moves.append(self.right_passant_end)
            self.can_right_passant = True
    
    def move(self, pos: tuple[int, int]) -> None:
        """Pawn must update its passant when moved"""
        super().move(pos)

        # UPDATE PASSANT
        self.left_passant = (self.x-1, self.en_passant_row)
        self.right_passant = (self.x+1, self.en_passant_row)
        self.left_passant_end = (self.x-1, self.en_passant_row+self.dir)
        self.right_passant_end = (self.x+1, self.en_passant_row+self.dir)
        self.left_passant_rect = self.get_rect(*self.left_passant_end)
        self.right_passant_rect = self.get_rect(*self.right_passant_end)