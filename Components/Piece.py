import pygame


class Piece:
    def __init__(self, owner_player, is_king=False, is_selected=False):
        self.is_king = is_king
        self.owner_player = owner_player
        self.is_selected = is_selected

    def draw(self, surface, point):
        pygame.draw.circle(surface, self.owner_player.color, point, 20)

        if self.is_king:
            pygame.draw.circle(surface, pygame.Color("yellow"), point, 10)
