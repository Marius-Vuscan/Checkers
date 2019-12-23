import pygame
from Helpers.DrawHelper import DrawHelper
from Components.Tile import Tile
from Components.Piece import Piece
from Components.Player import Player
from Helpers.MatrixHelper import MatrixHelper
from Model.Conquer import Conquer


class Board:
    def __init__(self, surface):
        self.surface = surface
        self.matrix = []
        self.player1 = Player(pygame.Color("black"), 1)
        self.player2 = Player(pygame.Color("white"), 2)
        self.init()

    def init(self):
        self.__init_tiles()
        self.__init_pieces()

    def draw(self):
        self.__draw_tiles()

    def __init_tiles(self):
        brown_color = (100, 40, 0)

        for x_axis_item in range(8):
            line = []
            for y_axis_item in range(8):
                point = (y_axis_item * 50 + 25, x_axis_item * 50 + 25)
                size = (50, 50)
                color = pygame.Color("white")

                if x_axis_item % 2 != y_axis_item % 2:
                    color = brown_color

                tile = Tile((point, size), color)
                line.append(tile)

            self.matrix.append(line)

    def __draw_tiles(self):
        brown_color = (100, 40, 0)
        pygame.draw.rect(self.surface, brown_color, ((0, 0), self.surface.get_size()))

        for x_axis_item in self.matrix:
            for y_axis_item in x_axis_item:
                y_axis_item.draw(self.surface)

        DrawHelper.draw_border_to_rectangle(self.surface, (25, 25, 400, 400), pygame.Color("black"), 5)

    def __init_pieces(self):
        for x_axis_item in self.matrix:
            player = None

            if self.matrix.index(x_axis_item) < 3:
                player = self.player1
            elif self.matrix.index(x_axis_item) > 4:
                player = self.player2

            if player is not None:
                for y_axis_item in x_axis_item:
                    if self.matrix.index(x_axis_item) % 2 != x_axis_item.index(y_axis_item) % 2:
                        piece = Piece(player)
                        y_axis_item.piece = piece

    def handle_board_click(self, position):
        for x_axis_item in self.matrix:
            for y_axis_item in x_axis_item:
                if y_axis_item.rect.collidepoint(position):
                    if self.__get_selected_tile() is not None:
                        self.__tile_on_click(y_axis_item, True)
                    else:
                        self.__tile_on_click(y_axis_item, False)

    def __reset_highlight(self):
        for x_axis_item in self.matrix:
            for y_axis_item in x_axis_item:
                y_axis_item.is_highlighted = False

    def __tile_on_click(self, tile, is_moving_action):
        # reset selected
        selected_tile = self.__get_selected_tile()
        if selected_tile is not None:
            selected_tile.piece.is_selected = False

        if is_moving_action:
            self.__move_piece(tile, selected_tile)
        else:
            self.__set_highlight(tile)
        self.__manage_piece_state()

    def __get_selected_tile(self):
        for x_axis_item in self.matrix:
            for y_axis_item in x_axis_item:
                if y_axis_item.piece is not None and y_axis_item.piece.is_selected:
                    return y_axis_item

    def __set_highlight(self, tile):
        self.__reset_highlight()
        if tile.piece is not None:
            tile.piece.is_selected = True

            available_tiles_to_move_array = self.__get_available_places_to_move_array(tile)
            available_tile_spots_to_conquer = self.__get_available_to_conquer_tiles(tile)

            for tile in available_tiles_to_move_array:
                tile.is_highlighted = True
            for tile in available_tile_spots_to_conquer:
                tile.available_spot_tile.is_highlighted = True

    def __get_available_to_conquer_tiles(self, tile):
        array = []
        (x, y) = MatrixHelper.get_matrix_index_of_element(self.matrix, tile)

        # first 2 positions are possible conquer sports for the first player and the second 2 are for the second player
        conquer_positions_array = [((x + 2, y + 2), (x + 1, y + 1)),
                                   ((x + 2, y - 2), (x + 1, y - 1)),
                                   ((x - 2, y - 2), (x - 1, y - 1)),
                                   ((x - 2, y + 2), (x - 1, y + 1))]

        iteration_index = 0
        for conquer_position in conquer_positions_array:
            if tile.piece.is_king \
                    or (self.matrix[x][y].piece.owner_player.player_id == 1 and iteration_index < 2) \
                    or (self.matrix[x][y].piece.owner_player.player_id == 2 and iteration_index > 1):
                (possible_spot_tile_x, possible_spot_tile_y) = conquer_position[0]
                (conquer_tile_x, conquer_tile_y) = conquer_position[1]

                valid_index = (0 <= possible_spot_tile_x < len(self.matrix) and 0 <= possible_spot_tile_y < len(
                    self.matrix[0]))
                if valid_index:
                    possible_spot_tile_is_empty = (self.matrix[possible_spot_tile_x][possible_spot_tile_y].piece is None)
                    conquer_tile_is_empty = (self.matrix[conquer_tile_x][conquer_tile_y].piece is None)
                    piece_owner_is_opponent = (self.matrix[conquer_tile_x][conquer_tile_y].piece is not None and self.matrix[x][y].piece is not None and
                                self.matrix[conquer_tile_x][conquer_tile_y].piece.owner_player is not self.matrix[x][y].piece.owner_player)

                    if possible_spot_tile_is_empty and not conquer_tile_is_empty and piece_owner_is_opponent:
                        array.append(Conquer(self.matrix[possible_spot_tile_x][possible_spot_tile_y], self.matrix[conquer_tile_x][conquer_tile_y]))
            iteration_index += 1
        return array

    def __move_piece(self, tile, selected_tile):
        available_tile_spots_to_move = self.__get_available_places_to_move_array(selected_tile)
        available_tile_spots_to_conquer = self.__get_available_to_conquer_tiles(selected_tile)

        if available_tile_spots_to_move.count(tile) > 0:
            tile.piece = selected_tile.piece
            selected_tile.piece = None

        for available_tile_spot_to_conquer in available_tile_spots_to_conquer:
            if available_tile_spot_to_conquer.available_spot_tile is tile:
                available_tile_spot_to_conquer.conquer_by_moving_tile.piece = None
                tile.piece = selected_tile.piece
                selected_tile.piece = None

        self.__reset_highlight()

    def __get_available_places_to_move_array(self, tile):
        array = []

        (x, y) = MatrixHelper.get_matrix_index_of_element(self.matrix, tile)
        move_positions_array = [(x + 1, y + 1),
                                (x + 1, y - 1),
                                (x - 1, y - 1),
                                (x - 1, y + 1)]
        iteration_index = 0

        for move_position_array in move_positions_array:
            if tile.piece.is_king \
                        or (self.matrix[x][y].piece.owner_player.player_id == 1 and iteration_index < 2) \
                        or (self.matrix[x][y].piece.owner_player.player_id == 2 and iteration_index > 1):
                (c_e_x, c_e_y) = move_position_array
                if 0 <= c_e_x < len(self.matrix) and 0 <= c_e_y < len(self.matrix[0]):
                    if self.matrix[c_e_x][c_e_y].piece is None:
                        array.append(self.matrix[c_e_x][c_e_y])
            iteration_index += 1

        return array


    def __manage_piece_state(self):
        """This method checks if a piece has reached the edge,
        if that happened then the piece status will be set to king."""

        for x_axis_item in self.matrix:
            for y_axis_item in x_axis_item:
                (x, y) = MatrixHelper.get_matrix_index_of_element(self.matrix, y_axis_item)
                if y_axis_item.piece is not None \
                    and ((y_axis_item.piece.owner_player.player_id == 1 and x == len(self.matrix) - 1) \
                    or (y_axis_item.piece.owner_player.player_id == 2 and x == 0)):
                        y_axis_item.piece.is_king = True
