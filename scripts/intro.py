import os
import pygame
import threading
from web.server import Server
from audio.mixer import Mixer
from scripts import ui, functions
from scripts.menu import OptionsMenu
from scripts.resolution import ResolutionScreen


class Intro:
    def __init__(self, screen: pygame.Surface, mixer: Mixer, path: str):

        # SCREEN CONFIGURATION
        self.screen = ResolutionScreen(screen, 1920, 1080)
        height = self.screen.get_height()

        # MUSIC
        self.mixer = mixer

        # BACKGROUND
        self.top = self.screen.convert(100)
        self.bottom = self.screen.convert(height-100)
        self.left = self.screen.convert(100)

        self.stars = ui.StarCluster(screen, 1000, max_radius=self.screen.convert(5))
        self.path = os.path.dirname(path)
        self.logo = self.screen.load_image(f'{self.path}/images/logo.png', color_key='black', scale=17.5)
        self.logo_rect = self.logo.get_rect(centerx=self.screen.width/2, top=height)

        # FONT
        self.font = pygame.font.Font(f'{self.path}/font/pixel.ttf', int(self.screen.convert(64)))

        # CLOCK
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        self.dt = 0

        # COORDINATION
        self.show_buttons = False
        self.no_continue = False

        # UI
        self.status_message = ''
        self.status_message_rect = None
        centerx = self.screen.width/2
        open_server = ui.Button(screen, self.font, 'Abrir partida', centerx, self.screen.convert(600), self.open_server)
        join_server = ui.Button(screen, self.font, 'Unirse a partida', centerx, self.screen.convert(664), self.join_server)
        options = ui.Button(screen, self.font, 'Opciones', centerx, self.screen.convert(728), self.options)
        exit_game = ui.Button(screen, self.font, 'Salir', centerx, self.screen.convert(792), self.leave)
        self.buttons = [
            open_server,
            join_server,
            options,
            exit_game
        ]

        # CONFIGURATION
        self.config = functions.Config(path)

        # MENUS
        self.show_options = False
        self.options_menu = OptionsMenu(self.screen, self)

    def leave(self) -> None:
        self.no_continue = True
    
    def open_server(self) -> None:
        server = Server()
        thread = threading.Thread(target=server.receive, daemon=True)
        thread.start()
        self.status_message = self.font.render('Servidor listo...'.upper(), True, 'white')
        self.status_message_rect = self.status_message.get_rect(left=self.left, bottom=self.bottom)
    
    def join_server(self) -> None:
        self.running = False

    def options(self) -> None:
        self.show_options = True

    def main(self) -> None:

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
                if event.type == pygame.QUIT: self.get_out()
                if event.type == pygame.USEREVENT: self.mixer.next()
                elif event.type == pygame.MOUSEMOTION: self.hover(event)
                elif event.type == pygame.MOUSEBUTTONDOWN: self.click(event)
            
            if self.show_options:
                self.options_menu.main()
                self.show_options = False

            self.update()
            self.show()
            pygame.display.update()
            self.dt = self.clock.tick(self.fps)

        # self.mixer.stop()
        return True
    
    def click(self, event: pygame.event) -> None:
        for button in self.buttons:
            button.click(event)
    
    def show(self) -> None:
        self.stars.show()
        self.screen.blit(self.logo, self.logo_rect)
        if not self.show_buttons: return
        for button in self.buttons: button.show()
        if self.status_message: self.screen.blit(self.status_message, self.status_message_rect)
    
    def update(self) -> None:
        if self.logo_rect.top > self.top: self.logo_rect = self.logo_rect.move(0, -10)
        elif not self.show_buttons: self.show_buttons = True
        self.stars.update(self.dt)
    
    def hover(self, event: pygame.event) -> None:
        for button in self.buttons:
            button.hover(event)