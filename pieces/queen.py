import pygame
from pieces.piece import Piece


class Queen(Piece):
    """Class Queen"""
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):

        # GET IMAGE BASED ON STARTING POSITION
        if team == 'white': image = 'leia'
        elif team == 'black': image = 'darth vader'
        
        super().__init__(board, screen, path, image, x, y, team, 'REINA')
    
    def calculate_moves(self) -> None:
        """Updates the list of possible moves"""
        self.possible_moves.clear()
        
        # DIRECTIONS
        front = [(self.x, y) for y in range(self.y-1, -1, -1)]
        back = [(self.x, y) for y in range(self.y+1, 8)]
        left = [(x, self.y) for x in range(self.x-1, -1, -1)]
        right = [(x, self.y) for x in range(self.x+1, 8)]
        topleft = [(self.x-i, self.y-i) for i in range(1, min(self.x, self.y)+1)]
        topright = [(self.x+j, self.y-j) for j in range(1, min(self.y, 7-self.x)+1)]
        bottomleft = [(self.x-k, self.y+k) for k in range(1, min(self.x, 7-self.y)+1)]
        bottomright = [(self.x+l, self.y+l) for l in range(1, min(7-self.x, 7-self.y)+1)]
        directions = [front, back, left, right, topleft, topright, bottomleft, bottomright]

        # CHECK DIRECTIONS
        for direction in directions: self.check_moves(direction)