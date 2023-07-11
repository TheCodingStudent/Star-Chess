import pygame
from pieces.piece import Piece


class Rook(Piece):
    """Class Rook"""
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):

        # GET IMAGE BASED ON STARTING POSITION
        if team == 'white':
            if x == 0: image = 'c3po'
            else: image = 'r2d2'
        elif team == 'black': image = 'officer'
        
        super().__init__(board, screen, path, image, x, y, team, 'TORRE')
    
    def calculate_moves(self) -> None:
        """Updates the list of possible moves"""
        self.possible_moves.clear()

        # DIRECTIONS
        front = [(self.x, y) for y in range(self.y-1, -1, -1)]
        back = [(self.x, y) for y in range(self.y+1, 8)]
        left = [(x, self.y) for x in range(self.x-1, -1, -1)]
        right = [(x, self.y) for x in range(self.x+1, 8)]
        directions = [front, back, left, right]

        # CHECK DIRECTIONS
        for direction in directions: self.check_moves(direction)