from pygame.constants import (
    K_ESCAPE,
    USEREVENT,
    QUIT,
    KEYDOWN,
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
    KMOD_NONE,
    KMOD_NUM,
)
from pygame.time import Clock, set_timer
from pygame.font import Font
from pygame.display import set_mode, set_caption, update
from pygame.event import get, wait
from pygame.image import load
from pygame import (
    init,
    quit as pgquit,
)
from random import randint

WIDTH = 800
HEIGHT = 150
UNI_IMAGE_PATH = r"data/uni.png"


class Tui10s:
    BUMP_TIMER = USEREVENT
    NUM_KEYS = {
        K_0: 0,
        K_1: 1,
        K_2: 2,
        K_3: 3,
        K_4: 4,
        K_5: 5,
        K_6: 6,
        K_7: 7,
        K_8: 8,
        K_9: 9,
    }

    class Colour:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

    def __init__(self, width, height, game_over_image_path):
        self.width = width
        self.height = height
        self.game_display = set_mode((self.width, self.height))
        set_caption("Tui's 10s")
        self.uni = load(game_over_image_path)
        self.clock = Clock()
        self.queue = []
        self.game_over = False

    def reset(self):
        self.queue = []
        self.game_over = False
        self.game_display.fill(self.Colour.WHITE)
        update()
        set_timer(self.BUMP_TIMER, 200)

    def killme(self):
        pgquit()
        quit()

    def draw_game_over(self):
        # Don't want this even cancelling the game over view
        set_timer(self.BUMP_TIMER, 0)
        text = "GAME OVER"
        large_text = Font("freesansbold.ttf", 100)
        text_surface = large_text.render(text, True, self.Colour.RED)
        text_rectangle = text_surface.get_rect().topleft = (
            170,
            25,
        )
        self.game_display.fill(self.Colour.WHITE)
        self.game_display.blit(self.uni, (0, 0))
        self.game_display.blit(text_surface, text_rectangle)
        update()
        while True:
            ke = wait()
            if ke.type == KEYDOWN:
                if ke.key == K_ESCAPE:
                    self.killme()
                # Only jump back from normal key presses
                if ke.mod == KMOD_NONE or ke.mod == KMOD_NUM:
                    break

    def redraw_queue(self):
        text = " ".join(str(e) for e in self.queue)
        large_text = Font("freesansbold.ttf", 115)
        text_surface = large_text.render(text, True, self.Colour.BLACK)
        text_rectangle = text_surface.get_rect()
        text_rectangle.top = 15
        text_rectangle.right = self.width
        if text_rectangle.left < 0:
            self.game_over = True
        else:
            self.game_display.fill(self.Colour.WHITE)
            self.game_display.blit(text_surface, text_rectangle)
            update()

    def drop(self):
        """Drop first element and re-draw"""
        self.queue.pop(0)
        self.redraw_queue()

    def bump(self):
        self.queue.append(randint(1, 9))
        self.redraw_queue()

    def game_loop(self):
        self.reset()
        while True:
            for event in get():
                if event.type == self.BUMP_TIMER:
                    self.bump()
                    if self.game_over:
                        self.draw_game_over()
                        self.reset()
                if event.type == KEYDOWN:
                    if event.key in self.NUM_KEYS.keys():
                        if len(self.queue) > 0:
                            if self.NUM_KEYS[event.key] == 10 - self.queue[0]:
                                self.drop()
                    elif event.key == K_ESCAPE:
                        self.killme()
                if event.type == QUIT:
                    self.killme()
            self.clock.tick(60)


if __name__ == "__main__":
    init()
    Tui10s(WIDTH, HEIGHT, UNI_IMAGE_PATH).game_loop()
    pgquit()
    quit()
