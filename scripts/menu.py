import pygame
from scripts.ui import Button


class OptionsMenu:
    def __init__(self, screen: pygame.Surface, intro):
        self.screen = screen
        self.intro = intro
        self.running = True
        self.dt = 0

        centerx = self.screen.get_width()/2
        centery = self.screen.get_height()/2
        height = self.screen.convert(64)

        numbers = tuple(range(101))

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
        self.running = False
    
    def update(self, dt: int) -> None:
        self.intro.stars.update(dt)
    
    def main(self) -> None:
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
        self.exit_button.click(event)
        for option in self.options:
            option.click(event)
    
    def hover(self, event: pygame.event) -> None:
        self.exit_button.hover(event)
        for option in self.options:
            option.hover(event)
    
    def show(self) -> None:
        self.exit_button.show()
        self.intro.stars.show()
        for option in self.options:
            option.show()


class Option:
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

        self.left_button = Button(screen, intro.font, '-', self.text_rect.left-10, self.text_rect.top, lambda: None, position='topright')
        self.right_button = Button(screen, intro.font, '+', self.text_rect.right+10, self.text_rect.top, lambda: None, position='topleft')
    
    def click(self, event: pygame.event) -> None:
        if left := self.left_button.click(event): self.index = (self.index-1) % len(self.options)
        if right := self.right_button.click(event): self.index = (self.index+1) % len(self.options)
        if left or right:
            self.config.update(self.variable, self.option)
            self.function(self.option)
            self.render()
    
    def hover(self, event: pygame.event) -> None:
        self.left_button.hover(event)
    
    def show(self) -> None:
        self.screen.blit(self.text, self.text_rect)
        self.left_button.show()
        self.right_button.show()
    
    def render(self):
        self.option = self.options[self.index]
        text = f'{self.string}: {self.option}'
        self.text = self.font.render(text, True, 'yellow', 'black')
        self.text_rect = self.text.get_rect(center=self.center)