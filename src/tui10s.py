import pygame

# from pygame.constants import (
#     USEREVENT,
#     NUMEVENTS,
#     QUIT,
#     KEYDOWN,
#     K_0,
#     K_1,
#     K_2,
#     K_3,
#     K_4,
#     K_5,
#     K_6,
#     K_7,
#     K_8,
#     K_9,
#     K_UP,
#     K_DOWN,
#     K_ESCAPE,
#     K_SPACE,
#     KMOD_NONE,
#     KMOD_NUM,
# )
# from pygame import time
# from pygame.font import Font
# from pygame.display import set_mode, set_caption, update
# from pygame.event import get, wait, clear
# from pygame.image import load
# from pygame import (
#     init,
#     quit as pgquit,
# )
from random import randint

WIDTH = 800
HEIGHT = 150
UNI_IMAGE_PATH = r"data/uni.png"


class Tui10s:
    INTERVAL_LIMITS = {"min": 200, "max": 10000}
    NUM_KEYS = {
        pygame.K_0: 0,
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
    }

    class Colour:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

    def __init__(
        self,
        width,
        height,
        game_over_image_path,
        interval=2000,
        cant_die=False,
        debug=False,
    ):
        pygame.init()
        self.width = width
        self.height = height
        self.game_display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tui's 10s")
        self.uni = pygame.image.load(game_over_image_path)
        self.clock = pygame.time.Clock()
        self.queue = []
        self.game_over = False
        self.interval = interval
        self.cant_die = cant_die
        self.bump_timer = pygame.USEREVENT
        self._play = True
        self.debug = debug

    def _reset(self):
        self.queue = []
        self.game_over = False
        self.game_display.fill(self.Colour.WHITE)
        pygame.display.update()
        self._stop_bump_timer()
        self._start_bump_timer()

    def _stop_bump_timer(self):
        pygame.time.set_timer(self.bump_timer, 0)
        pygame.event.clear(self.bump_timer)

    def _start_bump_timer(self):
        print(f"bump_timer now using {self.interval}")
        pygame.time.set_timer(self.bump_timer, self.interval)

    # def _update_timer(self, slow_down=False):
    #     change = -1000
    #     if slow_down:
    #         change = 1000
    #     self.interval = self.interval + change
    #     if self.interval < self.INTERVAL_LIMITS["min"]:
    #         self.interval = self.INTERVAL_LIMITS["min"]
    #     elif self.interval > self.INTERVAL_LIMITS["max"]:
    #         self.interval = self.INTERVAL_LIMITS["max"]
    #     self._stop_bump_timer()
    #     self._start_bump_timer()

    def _draw_game_over(self):
        self._stop_bump_timer()
        text = "GAME OVER"
        large_text = pygame.font.Font("freesansbold.ttf", 100)
        text_surface = large_text.render(text, True, self.Colour.RED)
        text_rectangle = text_surface.get_rect().topleft = (
            170,
            25,
        )
        self.game_display.fill(self.Colour.WHITE)
        self.game_display.blit(self.uni, (0, 0))
        self.game_display.blit(text_surface, text_rectangle)
        pygame.display.update()
        while True:
            ke = pygame.event.wait()
            if ke.type == pygame.KEYDOWN:
                if ke.key == pygame.K_ESCAPE:
                    self._play = False
                    break
                # Only jump back from normal key presses
                if ke.mod == pygame.KMOD_NONE or ke.mod == pygame.KMOD_NUM:
                    break

    def _redraw_queue(self):
        text = " ".join(str(e) for e in self.queue)
        large_text = pygame.font.Font("freesansbold.ttf", 115)
        text_surface = large_text.render(text, True, self.Colour.BLACK)
        text_rectangle = text_surface.get_rect()
        text_rectangle.top = 15
        text_rectangle.right = self.width
        if text_rectangle.left < 0:
            self.game_over = True
        else:
            self.game_display.fill(self.Colour.WHITE)
            self.game_display.blit(text_surface, text_rectangle)
            pygame.display.update()

    def _drop(self, all=False):
        """Drop first element and re-draw"""
        if all:
            self.queue.clear()
        else:
            self.queue.pop(0)
        self._redraw_queue()

    def _bump(self):
        if (not self.cant_die) or (self.cant_die and len(self.queue) < 8):
            self.queue.append(randint(1, 9))
        self._redraw_queue()

    def _game_loop(self):
        self._play = True
        self._reset()
        while self._play:
            for event in pygame.event.get():
                if event.type == self.bump_timer:
                    self._bump()
                    if self.game_over:
                        self._draw_game_over()
                        self._reset()
                if event.type == pygame.KEYDOWN:
                    if event.key in self.NUM_KEYS.keys():
                        if len(self.queue) > 0:
                            if self.NUM_KEYS[event.key] == 10 - self.queue[0]:
                                self._drop()
                    elif event.key == pygame.K_SPACE and self.debug:
                        self._drop(True)
                    # elif event.key == pygame.K_UP:
                    #     self._update_timer()
                    # elif event.key == pygame.K_DOWN:
                    #     self._update_timer(True)
                    elif event.key == pygame.K_ESCAPE:
                        self._play = False
                if event.type == pygame.QUIT:
                    self._play = False
            self.clock.tick(10)

    def play(self):
        self._game_loop()
        pygame.quit()


if __name__ == "__main__":
    Tui10s(WIDTH, HEIGHT, UNI_IMAGE_PATH).play()
    quit()
