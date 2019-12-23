import pygame
from Helpers.DrawHelper import DrawHelper


class Tile:
    def __init__(self, rect, color, piece=None, is_highlighted=False):
        self.rect = pygame.Rect(rect)
        self.piece = piece
        self.is_highlighted = is_highlighted
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        if self.piece is not None:
            self.piece.draw(surface, self.rect.center)

        if self.is_highlighted:
            DrawHelper.draw_border_to_rectangle(surface, self.rect, pygame.Color("yellow"), 4)
