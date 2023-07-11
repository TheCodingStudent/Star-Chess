import os
import pygame
import threading
import webbrowser
from web.server import Server
from audio.mixer import Mixer
from scripts import ui, functions
from scripts.resolution import ResolutionScreen
from scripts.menu import OptionsMenu, InstructionsMenu, GreetingsMenu


class Intro:
    """Manages the start menu"""
    def __init__(self, screen: pygame.Surface, mixer: Mixer, path: str):

        # LINKS
        self.issues = 'https://github.com/TheCodingStudent/Star-Chess/issues'

        # SCREEN CONFIGURATION
        self.screen = ResolutionScreen(screen, 1920, 1080)
        width, height = self.screen.get_size()

        # MUSIC
        self.mixer = mixer

        # BACKGROUND
        self.top = self.screen.convert(100)
        self.bottom = height - self.screen.convert(100)
        self.right = width - self.screen.convert(100)
        self.left = self.screen.convert(100)

        self.stars = ui.StarCluster(screen, 1000, max_radius=self.screen.convert(5))
        self.path = os.path.dirname(path)
        self.logo = self.screen.load_image(f'{self.path}/images/logo.png', color_key='black', scale=17.5)
        self.logo_rect = self.logo.get_rect(centerx=self.screen.width/2, top=height)

        # FONT
        self.font = pygame.font.Font(f'{self.path}/font/pixel.ttf', int(self.screen.convert(56)))

        # CLOCK
        self.clock = pygame.time.Clock()
        self.fps = 144
        self.dt = 0

        # UI
        centerx = self.screen.width/2
        open_server = ui.Button(screen, self.font, 'Abrir partida', centerx, self.screen.convert(600), self.open_server)
        join_server = ui.Button(screen, self.font, 'Unirse a partida', centerx, self.screen.convert(664), self.join_server)
        instructions = ui.Button(screen, self.font, 'Instrucciones', centerx, self.screen.convert(728), self.instructions)
        greetings = ui.Button(screen, self.font, 'Agradecimientos', centerx, self.screen.convert(792), self.greetings)
        options = ui.Button(screen, self.font, 'Opciones', centerx, self.screen.convert(856), self.options)
        exit_game = ui.Button(screen, self.font, 'Salir', centerx, self.screen.convert(920), self.leave)

        report_bug = ui.Button(
            screen, self.font, 'Reportar error', self.right, self.bottom,
            self.report_bug, position='bottomright',
            color='#ff0000', hover_color='#7f0000'
        )

        self.buttons = [
            open_server,
            join_server,
            instructions,
            greetings,
            options,
            exit_game,
            report_bug
        ]

        # CONFIGURATION
        self.config = functions.Config(path)

        # MENUS
        self.options_menu = OptionsMenu(self.screen, self)
        self.instructions_menu = InstructionsMenu(self.screen, self)
        self.greetings_menu = GreetingsMenu(self.screen, self)

        # ANIMATIONS
        self.title_anim = functions.DeltaValue(1000, height, self.top)

        # OTHER CHANGES
        # self.reset()

    def reset(self) -> None:
        """Resets the intro"""
        self.running = True
        self.show_options = False
        self.show_instructions = False
        self.show_greetings = False

        # COORDINATION
        self.running = True
        self.show_buttons = False
        self.no_continue = False

        # UI
        self.status_message = ''
        self.status_message_rect = None

    def report_bug(self) -> None:
        """Opens the issues tab on browser"""
        webbrowser.open(self.issues)

    def leave(self) -> None:
        """Exits all the game"""
        self.no_continue = True
    
    def open_server(self) -> None:
        """Opens the socket server"""
        server = Server()
        thread = threading.Thread(target=server.receive, daemon=True)
        thread.start()
        self.status_message = self.font.render('Servidor listo...'.upper(), True, 'white')
        self.status_message_rect = self.status_message.get_rect(left=self.left, bottom=self.bottom)
    
    def join_server(self) -> None:
        """Joins to a socket server"""
        self.running = False

    def options(self) -> None:
        """Activates the flag to show options"""
        self.show_options = True

    def instructions(self) -> None:
        """Activates the flag to show instructions"""
        self.show_instructions = True

    def greetings(self) -> None:
        """Activates the flag to show greetings"""
        self.show_greetings = True

    def main(self) -> None:
        """Main loop for the intro"""

        # MUSIC
        intro_path =  functions.resource_path(f'{self.path}/audio/music/Star Wars.mp3')
        self.mixer.set_music_volume(self.config.get('music_volume'))
        self.mixer.set_sound_volume(self.config.get('sound_volume'), play_sound=False)
        self.mixer.start(intro_path)
        self.mixer.play()

        # MAIN LOOP
        while self.running:
            if self.no_continue: return False
            self.screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.leave()
                if event.type == pygame.USEREVENT: self.mixer.next()
                elif event.type == pygame.MOUSEMOTION: self.hover(event)
                elif event.type == pygame.MOUSEBUTTONDOWN: self.click(event)
            
            if self.show_options:
                self.options_menu.main()
                self.show_options = False
            elif self.show_instructions:
                self.instructions_menu.main()
                self.show_instructions = False
            elif self.show_greetings:
                self.greetings_menu.main()
                self.show_greetings = False

            self.update()
            self.show()
            pygame.display.update()
            self.dt = self.clock.tick(self.fps)

        # self.mixer.stop()
        return True
    
    def click(self, event: pygame.event) -> None:
        """Checks if any button was pressed"""
        for button in self.buttons:
            button.click(event)
    
    def show(self) -> None:
        """Draws everything on screen"""
        self.stars.show()
        self.screen.blit(self.logo, self.logo_rect)
        if not self.show_buttons: return
        for button in self.buttons: button.show()
        if self.status_message: self.screen.blit(self.status_message, self.status_message_rect)
    
    def update(self) -> None:
        """Updates the animations"""
        if self.logo_rect.top != self.top:
            self.title_anim.update(self.dt)
            self.logo_rect.top = self.title_anim.value
        elif not self.show_buttons: self.show_buttons = True
        self.stars.update(self.dt)
    
    def hover(self, event: pygame.event) -> None:
        """Checks if the mouse is hovering any button"""
        for button in self.buttons:
            button.hover(event)