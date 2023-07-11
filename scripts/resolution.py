import pygame


class ResolutionScreen:
    def __init__(
        self, screen: pygame.Surface,
        origin_width: int, origin_height: int,
    ):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        width_ratio = self.width/origin_width
        height_ratio = self.height/origin_height
        self.ratio = min(width_ratio, height_ratio)

        self.center = pygame.Vector2(origin_width/2, origin_height/2)
    
    def load_image(self, image_path: str, color_key: object=None, scale: float=1) -> pygame.Surface:
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale_by(image, scale*self.ratio)
        if color_key: image.set_colorkey(color_key)
        return image

    def get_rect(self, image: pygame.Surface, coordinate: tuple[int, int], pos: str='topleft', adapt: bool=True) -> pygame.Rect:
        if adapt: dest = pygame.Vector2(coordinate) * self.ratio
        else: dest = coordinate
        return image.get_rect(**{pos:dest})

    def blit(self, surface: pygame.Surface, coordinate: tuple[int, int]) -> None:
        dest_coordinate = self.convert(coordinate)
        self.screen.blit(surface, dest_coordinate)
    
    def convert(self, value: object) -> object:
        if isinstance(value, pygame.Rect): return value
        if isinstance(value, (tuple, list)): value = pygame.Vector2(value)
        return value * self.ratio

    def fill(self, color: str) -> None:
        self.screen.fill(color)
    
    def draw_circle(self, color: str|tuple[int, int, int], center: tuple[int, int], radius: float, width: int=0) -> None:
        dest_center = self.convert(center)
        dest_radius = int(self.convert(radius))
        dest_width = int(self.convert(radius))
        pygame.draw.circle(self.screen, color, dest_center, dest_radius, dest_width)
    
    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def get_size(self) -> tuple[float, float]:
        return (self.width, self.height)