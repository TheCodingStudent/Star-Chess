import pygame
from pieces.rook import Rook
from pieces.piece import Piece

class King(Piece):
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):

        # GET IMAGE BASED ON STARTING POSITION
        if team == 'white': image = 'luke'
        elif team == 'black': image = 'palpatine'
        
        super().__init__(board, screen, path, image, x, y, team, 'REY')

        # PROPERTIES
        self.in_check = False

        # CASTLING
        self.can_left_castling = False
        self.can_right_castling = False
        self.left_rook = (0, self.y)
        self.right_rook = (7, self.y)
        self.left_castling = (self.x-2, self.y)
        self.right_castling = (self.x+2, self.y)
        self.left_rook_end = (self.x-1, self.y)
        self.right_rook_end = (self.x+1, self.y)
        self.left_castling_rect = self.get_rect(*self.left_castling)
        self.right_castling_rect = self.get_rect(*self.right_castling)
    
    def calculate_moves(self) -> None:
        self.possible_moves.clear()

        # MOVES
        moves = [
            (self.x-1, self.y-1),
            (self.x, self.y-1),
            (self.x+1, self.y-1),
            (self.x-1, self.y),
            (self.x+1, self.y),
            (self.x-1, self.y+1),
            (self.x, self.y+1),
            (self.x+1, self.y+1),
        ]

        # CHECK MOVES
        for move in moves:
            if self.available(move): self.possible_moves.append(move)
            elif self.is_enemy(move): self.possible_moves.append(move)
        
        # LEFT CASTLING
        self.can_left_castling = self.check_castling(self.left_rook)
        if self.can_left_castling: self.possible_moves.append(self.left_castling)

        # RIGHT CASTLING
        self.can_right_castling = self.check_castling(self.right_rook)
        if self.can_right_castling: self.possible_moves.append(self.right_castling)

    
    def check_castling(self, rook_pos: tuple[int, int]) -> bool:

        # CHECK PIECES PROPERTIES
        if self.moved or self.in_check: return False
        if not (rook := self.board.get(rook_pos)): return False
        if rook.moved: return False

        # CHECK IN BETWEEN PIECES
        if rook_pos[0] == 0: middle_pieces = [(1, self.y), (2, self.y), (3, self.y)]
        elif rook_pos[0] == 7: middle_pieces = [(5, self.y), (6, self.y)]
        for pos in middle_pieces:
            if not self.available(pos): return False
            if self.in_attack(pos): return False

        return True