import pygame
from pieces.piece import Piece


class Knight(Piece):
    """Class Knight"""
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):

        # GET IMAGE BASED ON STARTING POSITION
        if team == 'white':
            if x == 1: image = 'yoda'
            else: image = 'obi wan'
        elif team == 'black':
            if x == 1: image = 'boba fett'
            else: image = 'jango fett'
            
        super().__init__(board, screen, path, image, x, y, team, 'CABALLO')
    
    def calculate_moves(self) -> None:
        """Updates the list of possible moves"""
        self.possible_moves.clear()

        # MOVES
        moves = [
            (self.x-1, self.y-2),
            (self.x+1, self.y-2),
            (self.x-2, self.y-1),
            (self.x+2, self.y-1),
            (self.x-1, self.y+2),
            (self.x+1, self.y+2),
            (self.x-2, self.y+1),
            (self.x+2, self.y+1)
        ]

        # CHECK EACH MOVE
        for move in moves:
            if self.available(move): self.possible_moves.append(move)
            elif self.is_enemy(move): self.possible_moves.append(move)