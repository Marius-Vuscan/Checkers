import pygame
from Components.Board import Board


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 450, 450
        self.board = None
        self.display = None

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.display = pygame.display
        self.display.set_caption("Checkers")
        self.board = Board(self._display_surf)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                self.board.handle_board_click(event.pos)

    def on_loop(self):
        self.board.draw()
        self.display.update()

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()


