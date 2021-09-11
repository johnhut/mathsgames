import pygame
from random import randint

NUM_ADD_INTERVAL = 3000
WIDTH = 800
HEIGHT = 150
UNI_IMAGE_PATH = r"data/uni.png"
STAR_UNI_IMAGE_PATH = r"data/staruni.PNG"


class Tui10s:
    INTERVAL_LIMITS = {"min": 200, "max": 10000}
    END_SCREEN_MIN_TIME = 1000
    NUM_KEYS = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
        pygame.K_KP_1: 1,
        pygame.K_KP_2: 2,
        pygame.K_KP_3: 3,
        pygame.K_KP_4: 4,
        pygame.K_KP_5: 5,
        pygame.K_KP_6: 6,
        pygame.K_KP_7: 7,
        pygame.K_KP_8: 8,
        pygame.K_KP_9: 9,
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
        winning_image_path,
        interval=3000,
        cant_die=False,
        debug=False,
    ):
        pygame.init()
        self._width = width
        self._height = height
        self._game_display = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Tui's Number Pairs")
        self._images = {}
        self._images["lose"] = pygame.image.load(game_over_image_path)
        self._images["win"] = pygame.image.load(winning_image_path)
        self._clock = pygame.time.Clock()
        self._queue = []
        self._game_over = False
        self._bump_timer = pygame.USEREVENT
        self._interval = interval
        self._cant_die = cant_die
        self._debug = debug
        self._play = True
        self._start_bump_timer()
        self._start_time = pygame.time.get_ticks()

    def _reset(self):
        self._start_time = pygame.time.get_ticks()
        self._queue = []
        self._game_over = False
        self._game_display.fill(self.Colour.WHITE)
        pygame.display.update()

    def _clear_timer_events(self):
        pygame.event.clear(self._bump_timer)

    def _start_bump_timer(self):
        print(f"Adding numbers every {self._interval}ms.")
        pygame.time.set_timer(self._bump_timer, self._interval)

    def _wait_for_key(self, min_time=0):
        if min_time:
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < min_time:
                self._clock.tick(10)
        pygame.event.clear()
        while True:
            ke = pygame.event.wait()
            if ke.type == pygame.KEYDOWN:
                if ke.key == pygame.K_ESCAPE:
                    self._play = False
                    break
                # Only jump back from normal key presses
                if ke.mod == pygame.KMOD_NONE or ke.mod == pygame.KMOD_NUM:
                    break

    def _draw_game_over(self):
        text = "GAME OVER"
        large_text = pygame.font.Font("freesansbold.ttf", 100)
        text_surface = large_text.render(text, True, self.Colour.RED)
        text_rectangle = text_surface.get_rect().topleft = (
            170,
            25,
        )
        self._game_display.fill(self.Colour.WHITE)
        self._game_display.blit(self._images["lose"], (0, 0))
        self._game_display.blit(text_surface, text_rectangle)
        pygame.display.update()
        self._wait_for_key(self.END_SCREEN_MIN_TIME)

    def _draw_win(self):
        self._game_display = pygame.display.set_mode(
            (self._images["win"].get_width(), self._images["win"].get_height())
        )
        self._game_display.fill(self.Colour.BLACK)
        self._game_display.blit(self._images["win"], (0, 0))
        pygame.display.update()
        self._wait_for_key(self.END_SCREEN_MIN_TIME)
        self._game_display = pygame.display.set_mode((self._width, self._height))
        self._reset()

    def _redraw_queue(self):
        if not self._queue and (pygame.time.get_ticks() - self._start_time > 30000):
            self._draw_win()
            return
        text = " ".join(str(e) for e in self._queue)
        large_text = pygame.font.Font("freesansbold.ttf", 115)
        text_surface = large_text.render(text, True, self.Colour.BLACK)
        text_rectangle = text_surface.get_rect()
        text_rectangle.top = 15
        text_rectangle.right = self._width
        if text_rectangle.left < 0:
            self._game_over = True
        else:
            self._game_display.fill(self.Colour.WHITE)
            self._game_display.blit(text_surface, text_rectangle)
            pygame.display.update()

    def _drop(self, all=False):
        """Drop first element and re-draw"""
        if all:
            self._queue.clear()
        else:
            self._queue.pop(0)
        self._redraw_queue()

    def _bump(self):
        if (not self._cant_die) or (self._cant_die and len(self._queue) < 8):
            self._queue.append(randint(1, 9))
        self._redraw_queue()

    def play(self):
        self._play = True
        self._reset()
        while self._play:
            for event in pygame.event.get():
                if event.type == self._bump_timer:
                    self._bump()
                    if self._game_over:
                        self._draw_game_over()
                        self._reset()
                if event.type == pygame.KEYDOWN:
                    if event.key in self.NUM_KEYS.keys():
                        if len(self._queue) > 0:
                            if self.NUM_KEYS[event.key] == 10 - self._queue[0]:
                                self._drop()
                    elif event.key == pygame.K_SPACE and self._debug:
                        self._drop(True)
                    elif event.key == pygame.K_ESCAPE:
                        self._play = False
                if event.type == pygame.QUIT:
                    self._play = False
            self._clock.tick(10)
        pygame.quit()


if __name__ == "__main__":
    Tui10s(
        WIDTH,
        HEIGHT,
        UNI_IMAGE_PATH,
        winning_image_path=STAR_UNI_IMAGE_PATH,
        interval=NUM_ADD_INTERVAL,
    ).play()
    quit()
