import os
import pygame
from screen import ui
from web import client
from scripts import functions
from audio.mixer import Mixer
from settings.settings import *
from screen.resolution import ResolutionScreen

from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.king import King
from pieces.queen import Queen
from pieces.knight import Knight
from pieces.bishop import Bishop


class Board:
    def __init__(self, screen: pygame.Surface, mixer: Mixer, path: str):
        # SCREEN CONFIGURATION
        self.path = path
        self.screen = ResolutionScreen(screen, 1920, 1080)

        # MUSIC
        self.mixer = mixer

        # BACKGROUND
        self.left_stars = ui.StarCluster(screen, 100, max_x=self.screen.convert(BOARD_LEFT-10))
        self.right_stars = ui.StarCluster(screen, 100, min_x=self.screen.convert(BOARD_RIGHT+10), max_y=self.screen.convert(PLANET_TOP))

        self.background = self.screen.load_image(f'{os.path.dirname(path)}/images/{BOARD_IMAGE}')
        self.rect = self.screen.get_rect(self.background, self.screen.center, 'center')

        # FONT
        font_path = functions.resource_path(f'{os.path.dirname(path)}/font/pixel.ttf')
        self.font = pygame.font.Font(font_path, int(self.screen.convert(96)))

        # CLOCK
        self.clock = pygame.time.Clock()
        self.fps = 144
        self.dt = 0

        # ANIMATIONS
        self.turn_anim = functions.DeltaValue(duration=2000, min_value=0, max_value=1)
        self.confeti = ui.Confeti(screen)

        # UI
        self.exit_button = ui.Button(
            screen=screen,
            font=self.font,
            text='X',
            x=self.screen.convert(20),
            y=self.screen.convert(20),
            command=self.leave,
            position='topleft',
            color='#ff0000',
            hover_color='#7f0000'
        )
    
    def connect(self, ip: str, port: int) -> None:
        """Base function to connect, just for OnlineBoard"""
    
    def leave(self) -> None:
        """Marks the running flag to exit the board"""
        self.running = False

    def reset(self) -> None:
        """Resets the board to its initial state"""
        screen = self.screen.screen
        self.running = True

        # BOARD
        self.board = [
            [None, None, None, None, None, None, None, None],
            [Pawn(self, screen, self.path, x, 1, 'black') for x in range(8)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            # [None, None, None, None, None, None, None, None],
            [Pawn(self, screen, self.path, x, 6, 'white') for x in range(8)],
            [None, None, None, None, None, None, None, None],
        ]

        # PIECES
        self.board[0][0] = Rook(self, screen, self.path, 0, 0, 'black')
        self.board[0][7] = Rook(self, screen, self.path, 7, 0, 'black')
        self.board[7][0] = Rook(self, screen, self.path, 0, 7, 'white')
        self.board[7][7] = Rook(self, screen, self.path, 7, 7, 'white')

        self.board[0][1] = Knight(self, screen, self.path, 1, 0, 'black')
        self.board[0][6] = Knight(self, screen, self.path, 6, 0, 'black')
        self.board[7][1] = Knight(self, screen, self.path, 1, 7, 'white')
        self.board[7][6] = Knight(self, screen, self.path, 6, 7, 'white')
        
        self.board[0][2] = Bishop(self, screen, self.path, 2, 0, 'black')
        self.board[0][5] = Bishop(self, screen, self.path, 5, 0, 'black')
        self.board[7][2] = Bishop(self, screen, self.path, 2, 7, 'white')
        self.board[7][5] = Bishop(self, screen, self.path, 5, 7, 'white')

        self.board[0][3] = Queen(self, screen, self.path, 3, 0, 'black')
        self.board[7][3] = Queen(self, screen, self.path, 3, 7, 'white')

        self.board[0][4] = King(self, screen, self.path, 4, 0, 'black')
        self.board[7][4] = King(self, screen, self.path, 4, 7, 'white')

        self.black_king = self.board[0][4]
        self.white_king = self.board[7][4]

        self.white_pieces = [piece for row in self.board for piece in row if piece and piece.team == 'white']
        self.black_pieces = [piece for row in self.board for piece in row if piece and piece.team == 'black']
        self.all_pieces = self.white_pieces + self.black_pieces

        # PROPERTIES
        self.selected = None
        self.current = 'white'
        self.white_move_color = self.board[0][0].alpha_rect(BLUE, 0.2)
        self.black_move_color = self.board[0][0].alpha_rect(RED, 0.2)
        self.white_moves_rects = list()
        self.black_moves_rects = list()

        # WINNER
        self.winner = None
        self.winner_rect = None

        # ANIMATIONS
        self.turn_anim.reset()
        self.confeti.reset()

    # HELPING METHODS
    def win(self, real_winner: str='') -> None:
        """Updates the winner"""

        # GET MESSAGE
        if real_winner: winner = 'la republica' if real_winner=='white' else 'el imperio'
        else: winner = 'la republica' if self.current=='white' else 'el imperio'
        message = f'{winner} gana!'.upper()

        # GET TEXT AND SURFACES
        self.winner = self.font.render(message, True, 'white')
        self.winner_background = pygame.Surface(self.winner.get_size())
        self.winner_background.fill('black')
        self.winner_background.set_alpha(127)
        center = (self.screen.width/2, self.screen.height/2)
        self.winner_rect = self.winner_background.get_rect(center=center)

        self.mixer.play_sound('win.mp3')

    def change_turn(self) -> None:
        """Manages the logic of changing turn"""
        last_turn = self.current
        pieces = getattr(self, f'{self.current}_pieces')
        for piece in pieces: piece.reset()

        self.current = 'black' if self.current == 'white' else 'white'
        self.turn_anim.reset()
        self.get_possible_moves()
        if not getattr(self, f'{self.current}_moves_rects'):
            self.win(last_turn)

    def kill(self, x: int, y: int) -> None:
        """Removes the piece from the board and plays its sound"""
        if not (piece := self.get((x, y))): return
        if piece in self.black_pieces: self.black_pieces.remove(piece)
        if piece in self.white_pieces: self.white_pieces.remove(piece)
        self.all_pieces.remove(piece)
        self.board[y][x] = None
        self.mixer.play_sound('capture.wav')

        # CHECK IF MATE
        if isinstance(piece, King): self.win()

    def get_white_moves(self, check_legal:bool=True) -> list:
        moves = list()
        for white_piece in self.white_pieces:
            white_piece.calculate_moves()
            if check_legal: white_piece.check_legal()
            moves.extend(white_piece.possible_moves)
        return moves
    
    def get_black_moves(self, check_legal: bool=True) -> list:
        moves = list()
        for black_piece in self.black_pieces:
            black_piece.calculate_moves()
            if check_legal: black_piece.check_legal()
            moves.extend(black_piece.possible_moves)
        return moves

    def get_possible_moves(self) -> None:
        self.white_moves_rects.clear()
        self.get_white_moves()
        for white_piece in self.white_pieces:
            self.white_moves_rects.extend(white_piece.possible_moves_rects)
        
        self.black_moves_rects.clear()
        self.get_black_moves()
        for black_piece in self.black_pieces:
            self.black_moves_rects.extend(black_piece.possible_moves_rects)

        self.white_king.in_check = self.white_king.rect in self.black_moves_rects
        self.black_king.in_check = self.black_king.rect in self.white_moves_rects

        for white_piece in self.white_pieces:
            if not self.white_king.in_check: continue
            if not white_piece.possible_moves: white_piece.blocked = True

        for black_piece in self.black_pieces:
            if not self.black_king.in_check: continue
            if not black_piece.possible_moves: black_piece.blocked = True

    def move(self, x0: int, y0: int, x1: int, y1: int) -> None:
        """Manages the logic of moving a piece"""
        selected_piece = self.board[y0][x0]
        self.board[y0][x0], self.board[y1][x1] = self.board[y1][x1], self.board[y0][x0]
        selected_piece.move((x1, y1))
    
    def hover(self, event: pygame.event) -> None:
        """Manages the logic for hovering the board or piece"""
        current_pieces = getattr(self, f'{self.current}_pieces')
        self.exit_button.hover(event)
        for piece in current_pieces:
            piece.hover(event)
    
    def update(self, dt: int=0) -> None:
        """Updates all the visual elements"""
        self.left_stars.update(self.dt)
        self.right_stars.update(self.dt)
        self.turn_anim.update(self.dt)
        for piece in self.all_pieces:
            piece.update(self.dt)
        
        if self.winner: self.confeti.update(self.dt)

    def in_attack(self, pos: tuple[int, int]) -> bool:
        """Checks if the given position is in attack"""
        ...

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        """Checks if the given position is legal"""
        x, y = pos
        if (x < 0) or (x > 7): return False
        if (y < 0) or (y > 7): return False
        return True

    def available(self, pos: tuple[int, int]) -> bool:
        """Checks if the given position is available"""
        x, y = pos
        if not self.in_bounds(pos): return False
        return self.board[y][x] is None

    def get(self, pos: tuple[int, int]):
        """Returns the piece at the given position"""
        x, y = pos
        if not self.in_bounds(pos): return None
        return self.board[y][x]

    def show(self) -> None:
        """Draws the board on screen"""

        # SHOW BACKGROUND
        self.screen.blit(self.background, self.rect)
        self.left_stars.show()
        self.right_stars.show()

        # SHOW PIECES
        for white in self.white_pieces: white.show()
        for black in self.black_pieces: black.show()
        current_pieces = getattr(self, f'{self.current}_pieces')
        for piece in current_pieces:
            piece.show_moves()
            piece.show_name()
        
        # UPDATE TURN INDICATORS
        alpha = self.turn_anim.value
        if not self.winner:
            if self.current == 'white': color = GREY + (BLUE - GREY) * alpha
            else: color = GREY + (RED - GREY) * alpha
            top_color = color if self.current=='black' else GREY
            bottom_color = color if self.current=='white' else GREY
        else:
            top_color = bottom_color = RED if self.current=='white' else BLUE

        # DRAWS THE BOARD INDICATORS
        self.screen.draw_circle(top_color, TOPLEFT, 20)
        self.screen.draw_circle(top_color, TOPRIGHT, 20)
        self.screen.draw_circle(bottom_color, BOTTOMLEFT, 20)
        self.screen.draw_circle(bottom_color, BOTTOMRIGHT, 20)

        # UI
        self.exit_button.show()
    
        # DEBUG
        # enemy = 'black' if self.current=='white' else 'white'
        # rects = getattr(self, f'{enemy}_moves_rects')
        # color = getattr(self, f'{enemy}_move_color')
        # for rect in rects: self.screen.blit(color, rect)
        
        # SHOW WINNER
        if not self.winner: return
        self.screen.blit(self.winner_background, self.winner_rect)
        self.screen.blit(self.winner, self.winner_rect)
        self.confeti.show()
    
    def update_next_turn(self, x: int, y: int, attribute: str, value: object) -> None:
        piece = self.board[y][x]
        piece.update_next_turn(attribute, value)

    def click(self, event: pygame.event) -> None:
        """Manages all the logic when mouse is clicked"""

        # CHECK CLICK ON UI
        if self.exit_button.click(event): return

        # IF ANY WINNER THEN THE CLICK IS UNABLED
        if self.winner: return

        # GET ALL THE PIECES OF THE CURRENT PLAYER
        current_pieces = getattr(self, f'{self.current}_pieces')

        # APPLY ANY FLAG
        for piece in current_pieces:
            piece.check_flag()

        # CHECKS CLICK ON MOVE
        if self.selected:

            # KING SPECIAL MOVES
            if isinstance(self.selected, King):

                # LEFT CASTLING
                if self.selected.can_left_castling and self.selected.left_castling_rect.collidepoint(event.pos):
                    x, y = self.selected.left_castling
                    self.kill(x, y)
                    self.move(self.selected.x, self.selected.y, x, y)
                    x0, y0 = self.selected.left_rook
                    x1, y1 = self.selected.left_rook_end
                    self.move(x0, y0, x1, y1)
                    self.change_turn()
                    self.selected = None
                    return self.mixer.play_sound('castle.wav')

                # RIGHT CASTLING
                elif self.selected.can_right_castling and self.selected.right_castling_rect.collidepoint(event.pos):
                    x, y = self.selected.right_castling
                    self.move(self.selected.x, self.selected.y, x, y)
                    x0, y0 = self.selected.right_rook
                    x1, y1 = self.selected.right_rook_end
                    self.move(x0, y0, x1, y1)
                    self.change_turn()
                    self.selected = None
                    return self.mixer.play_sound('castle.wav')
            
            elif isinstance(self.selected, Pawn):

                # MOVED TWICE
                if self.selected.double_move_rect.collidepoint(event.pos) and not self.selected.moved:
                    self.selected.moved_twice = True
                    x, y = self.selected.x, self.selected.y
                    self.update_next_turn(x, y, "moved_twice", False)
                    x0, y0 = self.selected.x, self.selected.y
                    x1, y1 = self.selected.double_move
                    self.move(x0, y0, x1, y1)
                    self.change_turn()
                    self.selected = None
                    return

                # LEFT EN PASSANT
                elif self.selected.can_left_passant and self.selected.left_passant_rect.collidepoint(event.pos):
                    x, y = self.selected.left_passant
                    self.kill(x, y)
                    x0, y0 = self.selected.x, self.selected.y
                    x1, y1 = self.selected.left_passant_end
                    self.move(x0, y0, x1, y1)
                    self.change_turn()
                    self.selected = None
                    return

                # RIGHT EN PASSANT
                elif self.selected.can_right_passant and self.selected.right_passant_rect.collidepoint(event.pos):
                    x, y = self.selected.right_passant
                    self.kill(x, y)
                    x0, y0 = self.selected.x, self.selected.y
                    x1, y1 = self.selected.right_passant_end
                    self.move(x0, y0, x1, y1)
                    self.change_turn()
                    self.selected = None
                    return

            # CHECKS EACH POSSIBLE MOVE AND IF IT WAS CLICKED
            for i, rect in enumerate(self.selected.possible_moves_rects):
                if not rect.collidepoint(event.pos): continue
                x0, y0 = self.selected.x, self.selected.y
                x1, y1 = self.selected.possible_moves[i]
                self.kill(x1, y1)
                self.move(x0, y0, x1, y1)
                self.change_turn()
                self.selected = None
                return
            
            # IF NOT MOVE WAS SELECTED, THEN WE DESELECT THE PIECE
            self.selected.selected = False
            self.selected = None

        # CHECKS CLICK ON PIECE
        for piece in current_pieces:
            if not piece.click(event): continue
            if piece.blocked: continue
            self.selected = piece
            self.selected.calculate_moves()
            return self.selected.check_legal()

    def main(self) -> None:
        """Main loop of the board"""

        for piece in self.all_pieces:
            piece.calculate_moves()
            piece.check_legal()

        # MAIN LOOP
        while self.running:
            self.screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.USEREVENT: self.mixer.next()
                elif event.type == pygame.MOUSEMOTION: self.exit_button.hover(event)
                elif event.type == pygame.MOUSEBUTTONDOWN: self.exit_button.click(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n: self.mixer.next()
                    if event.key == pygame.K_m: self.win()

                # INTERACT UNLESS THERE IS A WINNER
                if not self.winner:
                    if event.type == pygame.MOUSEMOTION: self.hover(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN: self.click(event)

                # ONLY DETECT SPACEBAR TO RESET BOARD 
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                    self.reset()

            self.update()
            self.show()
            pygame.display.update()
            self.dt = self.clock.tick(self.fps)
        
    def tick(self) -> None:
        """Ticks the clock"""
        self.dt = self.clock.tick(self.fps)
    
    def promote(self, pawn, promotion_piece) -> None:
        """Promotes a pawn"""
        screen = self.screen.screen

        # print(self)
        x, y = pawn.x, pawn.y
        self.kill(x, y)
        new_piece = promotion_piece(self, screen, self.path, x, y, self.current)
        if self.current == 'white': self.white_pieces.append(new_piece)
        elif self.current == 'black': self.black_pieces.append(new_piece)
        self.all_pieces.append(new_piece)
        self.board[y][x] = new_piece

    def intro(self) -> None:
        """Loop for the intro animation"""

        # MAIN LOOP
        time = 0
        anim_time = 3000
        width = self.screen.get_width()
        left = self.screen.convert(LEFT)
        topleft = pygame.Vector2(LEFT, TOP)
        running = True

        pieces = list()
        for piece in self.all_pieces:
            start = pygame.Vector2(piece.x+0.5, piece.y+1)
            end =  self.screen.convert(start * SQUARE + topleft)
            pieces.append((piece, end))

        self.dt = self.clock.tick(self.fps)
        while running:
            self.screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.MOUSEMOTION: self.exit_button.hover(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.click(event): running = False
            
            self.left_stars.update(self.dt)
            self.right_stars.update(self.dt)
            self.screen.blit(self.background, self.rect)
            self.left_stars.show()
            self.right_stars.show()
            self.exit_button.show()

            if time > anim_time:
                time = anim_time
                running = False

            t = time/anim_time
            for (piece, end) in pieces:
                x = end.x + (width-left)*(1-t)
                piece.image_rect.centerx = x
                piece.image_rect.bottom = end.y
                piece.show()

            pygame.display.update()
            self.tick()
            time += self.dt
        
        self.main()
    
    def __repr__(self) -> str:
        return '\n'.join([' '.join([str(column) for column in row]) for row in self.board])


class OfflineBoard(Board):
    def __init__(self, screen: pygame.Surface, mixer: Mixer, path: str):
        super().__init__(screen, mixer, path)


class OnlineBoard(Board, client.Client):
    def __init__(self, screen: pygame.Surface, mixer: Mixer, path: str):
        Board.__init__(self, screen, mixer, path)
        client.Client.__init__(self)
    
    def on_receive(self, message: str) -> None:
        if message == 'connected': return
        function, args = message.split(':')
        function = getattr(self, function)
        if args: function(*eval(args))
        else: function()

    def kill(self, x: int, y: int) -> None:
        """Removes the piece from the board and plays its sound"""
        if not (piece := self.get((x, y))): return
        if piece in self.black_pieces: self.black_pieces.remove(piece)
        if piece in self.white_pieces: self.white_pieces.remove(piece)
        self.all_pieces.remove(piece)
        self.board[y][x] = None
        self.mixer.play_sound('capture.wav')

        # CHECK IF MATE
        if isinstance(piece, King): self.send_message(f'win:[]')
    
    def click(self, event: pygame.event) -> None:
        """Manages all the logic when mouse is clicked"""

        # CHECK CLICK ON UI
        if self.exit_button.click(event): return

        # IF ANY WINNER THEN THE CLICK IS UNABLED
        if self.winner: return

        # GET ALL THE PIECES OF THE CURRENT PLAYER
        current_pieces = getattr(self, f'{self.current}_pieces')

        # APPLY ANY FLAG
        for piece in current_pieces:
            piece.check_flag()

        # CHECKS CLICK ON MOVE
        if self.selected:

            # KING SPECIAL MOVES
            if isinstance(self.selected, King):

                # LEFT CASTLING
                if self.selected.can_left_castling and self.selected.left_castling_rect.collidepoint(event.pos):
                    x, y = self.selected.left_castling

                    self.send_message(f'kill:({x},{y})')
                    self.send_message(f'move:({self.selected.x},{self.selected.y},{x},{y})')
                    x0, y0 = self.selected.left_rook
                    x1, y1 = self.selected.left_rook_end
                    self.send_message(f'move:({x0},{y0},{x1},{y1})')
                    self.send_message(f'change_turn:[]', 0.1)
                    self.selected = None
                    return self.mixer.play_sound('castle.wav')

                # RIGHT CASTLING
                elif self.selected.can_right_castling and self.selected.right_castling_rect.collidepoint(event.pos):
                    x, y = self.selected.right_castling
                    self.send_message(f'move:({self.selected.x},{self.selected.y},{x},{y})')
                    x0, y0 = self.selected.right_rook
                    x1, y1 = self.selected.right_rook_end
                    self.send_message(f'move:({x0},{y0},{x1},{y1})')
                    self.send_message(f'change_turn:[]', 0.1)
                    self.selected = None
                    return self.mixer.play_sound('castle.wav')
            
            elif isinstance(self.selected, Pawn):

                # MOVED TWICE
                if self.selected.double_move_rect.collidepoint(event.pos) and not self.selected.moved:
                    self.selected.moved_twice = True
                    x, y = self.selected.x, self.selected.y
                    self.send_message(f'update_next_turn:({x},{y},"moved_twice",False)')
                    x1, y1 = self.selected.double_move
                    self.send_message(f'move:({x0},{y0},{x1},{y1})')
                    self.send_message(f'change_turn:[]', 0.1)
                    self.selected = None
                    return

                # LEFT EN PASSANT
                elif self.selected.can_left_passant and self.selected.left_passant_rect.collidepoint(event.pos):
                    x, y = self.selected.left_passant
                    self.send_message(f'kill:({x},{y})')
                    x0, y0 = self.selected.x, self.selected.y
                    x1, y1 = self.selected.left_passant_end
                    self.send_message(f'move:({x0},{y0},{x1},{y1})')
                    self.send_message(f'change_turn:[]', 0.1)
                    self.selected = None
                    return

                # RIGHT EN PASSANT
                elif self.selected.can_right_passant and self.selected.right_passant_rect.collidepoint(event.pos):
                    x, y = self.selected.right_passant
                    self.send_message(f'kill:({x},{y})')
                    x0, y0 = self.selected.x, self.selected.y
                    x1, y1 = self.selected.right_passant_end
                    self.send_message(f'move:({x0},{y0},{x1},{y1})')
                    self.send_message(f'change_turn:[]', 0.1)
                    self.selected = None
                    return

            # CHECKS EACH POSSIBLE MOVE AND IF IT WAS CLICKED
            for i, rect in enumerate(self.selected.possible_moves_rects):
                if not rect.collidepoint(event.pos): continue
                x0, y0 = self.selected.x, self.selected.y
                x1, y1 = self.selected.possible_moves[i]
                self.send_message(f'kill:({x1},{y1})')
                self.send_message(f'move:({x0},{y0},{x1},{y1})')
                self.send_message(f'change_turn:[]', 0.1)
                self.selected = None
                return
            
            # IF NOT MOVE WAS SELECTED, THEN WE DESELECT THE PIECE
            self.selected.selected = False
            self.selected = None

        # CHECKS CLICK ON PIECE
        for piece in current_pieces:
            if not piece.click(event): continue
            self.selected = piece
            self.selected.calculate_moves()
            return self.selected.check_legal()