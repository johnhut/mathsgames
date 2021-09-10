from pygame.time import Clock
from pygame.font import Font
from pygame.display import set_mode, set_caption, update
from pygame.event import get
from pygame import (
    init,
    quit as pgquit,
    QUIT,
    KEYDOWN,
    KEYUP,
    K_0,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
)
from enum import Enum
import time

WIDTH = 800
HEIGHT = 150


class Tui10s:
    class Colour():
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_display = set_mode((self.width, self.height))
        set_caption("Tui 10s")
        self.clock = Clock()

    def message_display(self, text):
        large_text = Font("freesansbold.ttf", 115)
        text_surface = large_text.render(text, True, self.Colour.BLACK)
        text_rectangle = text_surface.get_rect().center = (
            (self.width / 2),
            (self.height / 2),
        )
        self.game_display.blit(text_surface, text_rectangle)

        update()

        time.sleep(2)

        self.game_loop()

    def game_loop(self):
        x = self.width
        y = self.height * 0.1
        key_active = False

        gameExit = False

        while not gameExit:

            for event in get():
                if event.type == QUIT:
                    pgquit()
                    quit()

                if event.type == KEYDOWN:
                    if event.key == K_0:
                        key_active = K_0

                if event.type == KEYUP:
                    if event.key == K_0:
                        key_active = None

            self.game_display.fill(self.Colour.WHITE)

            update()
            self.clock.tick(60)


if __name__ == "__main__":
    init()
    Tui10s(WIDTH, HEIGHT).game_loop()
    pgquit()
    quit()
