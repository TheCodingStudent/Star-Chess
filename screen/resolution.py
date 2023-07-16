import pygame


class ResolutionScreen:
    """Class to handle all the transformation graphics of different resolution"""
    def __init__(
        self, screen: pygame.Surface,
        origin_width: int, origin_height: int,
    ):
        
        # PROPERTIES
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        width_ratio = self.width/origin_width
        height_ratio = self.height/origin_height
        self.ratio = min(width_ratio, height_ratio)
        self.center = pygame.Vector2(origin_width/2, origin_height/2)
    
    def load_image(self, image_path: str, color_key: object=None, scale: float=1) -> pygame.Surface:
        """Returns an scaled image"""
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale_by(image, scale*self.ratio)
        if color_key: image.set_colorkey(color_key)
        return image

    def get_rect(self, image: pygame.Surface, coordinate: tuple[int, int], pos: str='topleft', adapt: bool=True) -> pygame.Rect:
        """Returns an scaled red"""
        if adapt: dest = pygame.Vector2(coordinate) * self.ratio
        else: dest = coordinate
        return image.get_rect(**{pos:dest})

    def blit(self, surface: pygame.Surface, coordinate: tuple[int, int]) -> None:
        """Pastes a surface on screen"""
        dest_coordinate = self.convert(coordinate)
        self.screen.blit(surface, dest_coordinate)
    
    def convert(self, value: object) -> object:
        """Converts a value based on aspect ratio"""
        if isinstance(value, pygame.Rect): return value
        if isinstance(value, (tuple, list)): value = pygame.Vector2(value)
        return value * self.ratio

    def fill(self, color: str) -> None:
        """Fills the screen with the given color"""
        self.screen.fill(color)
    
    def draw_circle(self, color: str|tuple[int, int, int], center: tuple[int, int], radius: float, width: int=0) -> None:
        """Draws an scaled circle"""
        dest_center = self.convert(center)
        dest_radius = int(self.convert(radius))
        dest_width = int(self.convert(width))
        pygame.draw.circle(self.screen, color, dest_center, dest_radius, dest_width)
    
    def get_width(self) -> float:
        """Returns the current width"""
        return self.width

    def get_height(self) -> float:
        """Returns the current height"""
        return self.height

    def get_size(self) -> tuple[float, float]:
        """Returns the current size"""
        return (self.width, self.height)