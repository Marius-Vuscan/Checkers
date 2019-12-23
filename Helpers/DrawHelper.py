import pygame


class DrawHelper:
    @staticmethod
    def draw_border_to_rectangle(surface, rect, color, width):
        rectangle = pygame.Rect(rect)

        pygame.draw.line(surface, color, rectangle.topleft, rectangle.topright, width)
        pygame.draw.line(surface, color, rectangle.topleft, rectangle.bottomleft, width)
        pygame.draw.line(surface, color, rectangle.bottomleft, rectangle.bottomright, width)
        pygame.draw.line(surface, color, rectangle.topright, rectangle.bottomright, width)
