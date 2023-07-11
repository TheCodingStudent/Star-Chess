import pygame
from pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):

        # GET IMAGE BASED ON STARTING POSITION
        if team == 'white':
            if x == 2: image = 'chewbacca'
            else: image = 'han solo'
        elif team == 'black': image = 'guardian'
        
        super().__init__(board, screen, path, image, x, y, team, 'ALFIL')
    
    def calculate_moves(self) -> None:
        self.possible_moves.clear()

        topleft = [(self.x-i, self.y-i) for i in range(1, min(self.x, self.y)+1)]
        topright = [(self.x+j, self.y-j) for j in range(1, min(self.y, 7-self.x)+1)]
        bottomleft = [(self.x-k, self.y+k) for k in range(1, min(self.x, 7-self.y)+1)]
        bottomright = [(self.x+l, self.y+l) for l in range(1, min(7-self.x, 7-self.y)+1)]

        directions = [topleft, bottomleft, topright, bottomright]
        for direction in directions:
            self.check_moves(direction)