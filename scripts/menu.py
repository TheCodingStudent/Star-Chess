import pygame
from scripts.ui import Button


class Menu:
    """Menu template"""
    def __init__(self, screen: pygame.Surface, intro, name: str):

        # PROPERTIES
        self.screen = screen
        self.intro = intro
        self.running = True
        self.dt = 0
        self.options = list()

        # NAME
        top = self.screen.convert(50)
        self.name = self.intro.font.render(name.upper(), True, 'yellow')
        self.name_rect = self.name.get_rect(centerx=self.screen.get_width()/2, top=top)

        # UI
        self.exit_button = Button(
            screen=screen,
            font=self.intro.font,
            text='X',
            x=self.screen.convert(20),
            y=self.screen.convert(20),
            command=self.leave,
            position='topleft',
            color='#ff0000',
            hover_color='#7f0000'
        )

    def leave(self) -> None:
        """Exits the menu"""
        self.running = False
    
    def update(self, dt: int) -> None:
        """Updates the animations"""
        self.intro.stars.update(dt)
    
    def main(self) -> None:
        """Main loop of the menu"""

        while self.running:
            self.screen.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: self.click(event)
                elif event.type == pygame.MOUSEMOTION: self.hover(event)
            
            self.update(self.dt)
            self.show()

            pygame.display.update()
            self.dt = self.intro.clock.tick(self.intro.fps)

        self.running = True
    
    def click(self, event: pygame.event) -> None:
        """Checks if any button was clicked"""
        self.exit_button.click(event)
        for option in self.options:
            option.click(event)
    
    def hover(self, event: pygame.event) -> None:
        """Checks if the mouse is hovering any button"""
        self.exit_button.hover(event)
        for option in self.options:
            option.hover(event)
    
    def show(self) -> None:
        """Draws everything on screen"""
        self.screen.blit(self.name, self.name_rect)
        self.exit_button.show()
        self.intro.stars.show()
        for option in self.options:
            option.show()


class OptionsMenu(Menu):
    """Menu for the game configuration options"""
    def __init__(self, screen: pygame.Surface, intro):
        super().__init__(screen, intro, 'Opciones')

        # PROPERTIES
        centerx = self.screen.get_width()/2
        centery = self.screen.get_height()/2
        height = self.screen.convert(64)

        # VARIABLES
        numbers = tuple(range(101))

        # OPTIONS
        self.options = [
            Option(
                screen=screen,
                intro=intro,
                string='VOLUMEN DE LA MUSICA',
                center=(centerx, centery),
                options=numbers,
                config=self.intro.config,
                function=self.intro.mixer.set_music_volume,
                variable='music_volume'
            ),
            Option(
                screen=screen,
                intro=intro,
                string='VOLUMEN DE LOS SONIDOS',
                center=(centerx, centery+height),
                options=numbers,
                config=self.intro.config,
                function=self.intro.mixer.set_sound_volume,
                variable='sound_volume'
            )
        ]


class TextMenu(Menu):
    def __init__(self, screen: pygame.Surface, intro, lines: list[str], name: str):
        super().__init__(screen, intro, name)

        # PROPERTIES
        centerx = self.screen.get_width()/2
        centery = self.screen.get_height()/2

        # TEXT
        texts = [
            self.intro.font.render(line.upper(), True, 'yellow')
            for line in lines
        ]

        max_width = max([text.get_width() for text in texts]) 
        max_height = sum([text.get_height() for text in texts])

        self.text = pygame.Surface((max_width, max_height))
        self.text.set_colorkey('black')

        y = 0
        for text in texts:
            rect = text.get_rect(centerx=max_width/2, top=y)
            self.text.blit(text, rect)
            y += text.get_height()
        
        self.rect = self.text.get_rect(center=(centerx, centery))
    
    def show(self) -> None:
        """Draws everything on screen"""
        self.intro.stars.show()
        self.exit_button.show()
        self.screen.blit(self.text, self.rect)
        self.screen.blit(self.name, self.name_rect)


class InstructionsMenu(TextMenu):
    """Menu for the game configuration options"""
    def __init__(self, screen: pygame.Surface, intro):

        # LINES
        lines = [
            "1. Los menus tienen botones de salida, en caso de algun error",
            "utiliza Alt+F4 o Alt+Fn+F4.",
            " ",
            "2. Las piezas se mueven utilizando el mouse, da un click con el",
            "boton izquierdo y apareceran los movimientos legales que",
            "puedes realizar.",
            " ",
            "3. Si seleccionas un movimiento legal la pieza se movera a ese",
            "lugar, en cambio si seleccionas el tablero se quitara la",
            "seleccion de esa pieza.",
            " ",
            "4. Una vez haya algun ganador la forma de reiniciar el tablero",
            "es presionando la tecla de espacio.",
            " ",
            " ",
            "En caso de cualquier error por favor reportarlo haciendo uso",
            "del boton de reportar error en el menu de inicio. Te llevara",
            "a la pagina donde habra un boton verde para agregarlo"
        ]

        super().__init__(screen, intro, lines, 'Instrucciones')


class GreetingsMenu(TextMenu):
    def __init__(self, screen: pygame.Surface, intro):
        lines = [
            "Javier Vazquez",
            "Por probar el juego conmigo y darme feedback e inspirarme",
            "para seguir programando y mejorar como persona.",
            " ",
            "Demian Marin",
            "Por hacer el diseño del tablero y darme feedback igualmente,",
            "por las horas en llamada que pasamos mientras programo"
        ]

        super().__init__(screen, intro, lines, 'Agradecimientos')


class ServerMenu(Menu):
    def __init__(self, screen: pygame.Surface, intro, name: str):
        super().__init__(screen, intro, name)

        # PROPERTIES
        centerx = self.screen.get_width()/2
        centery = self.screen.get_height()/2
        height = self.screen.convert(64)

        # VARIABLES
        numbers = tuple(range(101))

        # OPTIONS
        self.options = [
            Option(
                screen=screen,
                intro=intro,
                string='VOLUMEN DE LA MUSICA',
                center=(centerx, centery),
                options=numbers,
                config=self.intro.config,
                function=self.intro.mixer.set_music_volume,
                variable='music_volume'
            ),
            Option(
                screen=screen,
                intro=intro,
                string='VOLUMEN DE LOS SONIDOS',
                center=(centerx, centery+height),
                options=numbers,
                config=self.intro.config,
                function=self.intro.mixer.set_sound_volume,
                variable='sound_volume'
            )
        ]


class Entry:
    """Class to handle text input"""
    def __init__(
            self, screen: pygame.Surface, intro, string: str,
            center: tuple[int, int]
    ):
        
        # STYLE
        self.screen = screen
        self.string = string
        self.font = intro.font
        self.center = center

    def render(self):
        """Renders the entry text and its current text"""
        self.option = self.options[self.index]
        text = f'{self.string}: {self.option}'
        self.text = self.font.render(text, True, 'yellow', 'black')
        self.background = pygame.Surface(self.text.get_size())
        self.text_rect = self.text.get_rect(center=self.center)
    
    def click(self, event: pygame.event) -> None:
        """Checks if any button was clicked"""
        if left := self.left_button.click(event): self.index = (self.index-1) % len(self.options)
        if right := self.right_button.click(event): self.index = (self.index+1) % len(self.options)
        if left or right:
            self.config.update(self.variable, self.option)
            self.function(self.option)
            self.render()
    
    def hover(self, event: pygame.event) -> None:
        """Checks if the mouse is hovering any button"""
        self.left_button.hover(event)
    
    def show(self) -> None:
        """Draws everything on screen"""
        self.screen.blit(self.text, self.text_rect)


class Option:
    """Class to handle an option"""
    def __init__(
            self, screen: pygame.Surface, intro, string: str,
            center: tuple[int, int], options: list,
            config, function: object=lambda value: None,
            variable: str=''
    ):
        
        # STYLE
        self.screen = screen
        self.string = string
        self.font = intro.font
        self.center = center

        # CONFIGURATION
        self.option = None
        self.options = options
        self.config = config
        self.variable = variable
        self.index = self.config.get(self.variable)
        self.function = function
        self.render()

        # UI
        self.left_button = Button(screen, intro.font, '-', self.text_rect.left-20, self.text_rect.top, lambda: None, position='topright')
        self.right_button = Button(screen, intro.font, '+', self.text_rect.right+20, self.text_rect.top, lambda: None, position='topleft')
    
    def click(self, event: pygame.event) -> None:
        """Checks if any button was clicked"""
        if left := self.left_button.click(event): self.index = (self.index-1) % len(self.options)
        if right := self.right_button.click(event): self.index = (self.index+1) % len(self.options)
        if left or right:
            self.config.update(self.variable, self.option)
            self.function(self.option)
            self.render()
    
    def hover(self, event: pygame.event) -> None:
        """Checks if the mouse is hovering any button"""
        self.left_button.hover(event)
    
    def show(self) -> None:
        """Draws everything on screen"""
        self.screen.blit(self.text, self.text_rect)
        self.left_button.show()
        self.right_button.show()
    
    def render(self):
        """Renders the option text and its current option"""
        self.option = self.options[self.index]
        text = f'{self.string}: {self.option}'
        self.text = self.font.render(text, True, 'yellow', 'black')
        self.text_rect = self.text.get_rect(center=self.center)