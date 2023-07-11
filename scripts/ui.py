import pygame
import random
import threading


class Star(pygame.Vector2):
    """A circle that changes its brightness with the time to simulate a star"""
    def __init__(
        self, screen: pygame.Surface,
        min_radius: int, max_radius: int,
        min_time: int, max_time: int,
        min_x: int, max_x: int,
        min_y: int, max_y: int
    ):
        
        x = (max_x-min_x) * random.random() + min_x
        y = (max_y-min_y) * random.random() + min_y
        super().__init__(x, y)

        # PROPERTIES
        self.screen = screen
        self.radius = (max_radius-min_radius)*random.random() + min_radius
        self.brightness = random.randint(0, 255)
        self.sign = 1
        self.light_time = 1000*(random.random() + random.randint(min_time, max_time))
        self.time = 0
    
    def show(self) -> None:
        """Draws a circle on screen"""
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(self.screen, color, self, self.radius)
    
    def update(self, dt: float) -> None:
        """Updates the brightness"""
        self.time += dt * self.sign
        if self.time > self.light_time:
            self.time = self.light_time
            self.sign = -1
        elif self.time < 0:
            self.time = 0
            self.sign = 1
        self.brightness = 255 * self.time/self.light_time


class StarCluster:
    """Collection of stars to simulate space"""
    def __init__(
        self, screen: pygame.Surface, num_stars: int,
        min_radius: int=0, max_radius: int=5,
        min_time: int=1, max_time: int=2,
        min_x: int=0, max_x: int=0,
        min_y: int=0, max_y: int=0
    ):
        
        # PROPERTIES
        if not max_x: max_x = screen.get_width()
        if not max_y: max_y = screen.get_height()

        # STARS
        properties = (screen, min_radius, max_radius, min_time, max_time, min_x, max_x, min_y, max_y)
        self.stars = [Star(properties) for _ in range(num_stars)]
    
    def show(self) -> None:
        """Draws each star on screen"""
        for star in self.stars:
            star.show()
    
    def update(self, dt: float) -> None:
        """Updates each star based on deltatime"""
        for star in self.stars:
            star.update(dt)


class Button:
    """Class to simulate a button"""
    def __init__(
        self, screen: pygame.Surface, font: pygame.font.Font,
        text: str, x: int, y: int, command: object, position: str='center',
        thread_it: bool=True, color: str='#ffff00', hover_color: str='#7f7f00'
    ):
        
        # STYLE PROPERTIES
        self.color = color
        self.hover_color = hover_color
        self.font = font

        # PROPERTIES
        self.screen = screen
        self.string = text.upper()
        self.text = font.render(text.upper(), True, 'yellow')
        self.rect = self.text.get_rect(**{position:(x, y)})
        self.command = command
        self.thread_it = thread_it
        self.hovered = False
    
    def show(self):
        """Draws the text on screen"""
        color = self.color if not self.hovered else self.hover_color
        self.text = self.font.render(self.string, True, color)
        self.screen.blit(self.text, self.rect)
    
    def click(self, event: pygame.event) -> bool:
        """Checks if the button was clicked and calls a function"""
        if not self.rect.collidepoint(event.pos): return False
        if not self.thread_it: return True
        thread = threading.Thread(target=self.command, daemon=True)
        thread.start()
        return True
    
    def hover(self, event: pygame.event) -> None:
        """Checks if the mouse is over the button"""
        if not self.rect.collidepoint(event.pos): self.hovered = False
        else: self.hovered = True