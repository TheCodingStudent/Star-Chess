import pygame
from pieces.rook import Rook
from pieces.piece import Piece
from pieces.queen import Queen
from pieces.knight import Knight
from pieces.bishop import Bishop
from settings.settings import GREEN


class Pawn(Piece):
    """Class Pawn"""
    def __init__(self, board, screen: pygame.Surface, path: str, x: int, y: int, team: 'str'):
        
        # GET IMAGE BASED ON STARTING POSITION
        image = 'rebel' if team == 'white' else 'death trooper'
        self.main_path = path
        super().__init__(board, screen, path, image, x, y, team, 'PEON')

        # PAWN PROPERTIES
        self.dir = -1 if team == 'white' else 1
        self.en_passant_row = 3 if team == 'white' else 4
        self.double_move = (self.x, self.y+2*self.dir)
        self.double_move_rect = self.get_rect(*self.double_move)
        self.moved_twice = False
        self.can_passant = False

        self.promotion_pos = (self.x, 0 if team=='white' else 7)
        self.left_passant = (self.x-1, self.en_passant_row)
        self.right_passant = (self.x+1, self.en_passant_row)
        self.left_passant_end = (self.x-1, self.en_passant_row+self.dir)
        self.right_passant_end = (self.x+1, self.en_passant_row+self.dir)
        self.promotion_rect = self.get_rect(*self.promotion_pos)
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
        if not hasattr(left_passant, 'moved_twice'): return
        
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

        # UPDATE PASSANT AND PROMOTION
        self.promotion_pos = (self.x, 0 if self.team=='white' else 7)
        self.left_passant = (self.x-1, self.en_passant_row)
        self.right_passant = (self.x+1, self.en_passant_row)
        self.left_passant_end = (self.x-1, self.en_passant_row+self.dir)
        self.right_passant_end = (self.x+1, self.en_passant_row+self.dir)
        self.left_passant_rect = self.get_rect(*self.left_passant_end)
        self.right_passant_rect = self.get_rect(*self.right_passant_end)

        # CHECK IF PROMOTION
        if (pos == self.promotion_pos) and (not self.board.winner):
            self.promotion()
    
    def promotion(self) -> None:
        """Opens the UI to promote the pawn"""
        running = True

        x = 8 if self.team=='white' else -1
        promotion_piece = None
        rook = Rook(None, self.screen, self.main_path, x, 2, self.team)
        queen = Queen(None, self.screen, self.main_path, x, 3, self.team)
        knight = Knight(None, self.screen, self.main_path, x, 4, self.team)
        bishop = Bishop(None, self.screen, self.main_path, x, 5, self.team)
        pieces = (rook, queen, knight, bishop)

        while running:
            self.screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rook.click(event): promotion_piece = Rook
                    elif queen.click(event): promotion_piece = Queen
                    elif knight.click(event): promotion_piece = Knight
                    elif bishop.click(event): promotion_piece = Bishop
                    if promotion_piece: running = False
                elif event.type == pygame.MOUSEMOTION:
                    for piece in pieces: piece.hover(event)

            self.board.update()
            self.board.show()

            self.screen.blit(rook.promotion_color, rook.rect)
            self.screen.blit(queen.promotion_color, queen.rect)
            self.screen.blit(knight.promotion_color, knight.rect)
            self.screen.blit(bishop.promotion_color, bishop.rect)

            for piece in pieces: piece.show()

            pygame.display.update()
            self.board.tick()
        
        self.board.promote(self, promotion_piece)