from Settings import *
from os import listdir
import time

# Constants
ALLOWED_FILES = ("png", "jpg", "jpeg", "webp")


def load_all_images(dir_path, size, reverseX=False, reverseY=False):
    paths = listdir(dir_path)
    all_images = []
    for path in paths:
        if path.split(".")[-1] in ALLOWED_FILES:
            img = py.transform.smoothscale(py.image.load(dir_path + path), size)
            img = py.transform.flip(img, reverseX, reverseY)
            all_images.append(img.convert_alpha())
    return all_images


class Animator:
    def __init__(self, **kwargs):
        self.anim = dict(kwargs)
        self.current_anim = "idle"
        self.anim[self.current_anim].start()

    def get_current_image(self):
        return self.anim[self.current_anim].get_current_frame()

    def update(self):
        for v in self.anim.values():
            v.update()

    def is_ended(self):
        return self.anim[self.current_anim].is_ended()

    def set_anim(self, anim):
        if anim == self.current_anim:
            return
        self.current_anim = anim
        self.anim[self.current_anim].start()


class Animation:
    def __init__(self, duration: float, *images, StopAtEnd=False):
        self.duration = duration
        self.images = list(images)
        self.StopAtEnd = StopAtEnd
        self.delay = self.duration / len(self.images)
        self.current_frame = 0
        self.next_frame = time.time_ns() + self.delay

    def is_ended(self):
        return self.current_frame + 1 == len(self.images)

    def get_current_frame(self):
        return self.images[self.current_frame]

    def start(self):
        self.current_frame = 0
        self.next_frame = time.time_ns() + self.delay

    def update(self):
        if time.time_ns() > self.next_frame:
            self.current_frame += 1
            if self.current_frame == len(self.images):
                if self.StopAtEnd:
                    self.current_frame -= 1
                else:
                    self.current_frame = 0
            self.next_frame = self.next_frame + self.delay


if __name__ == '__main__':
    ANIMATOR = Animator(
        player_idle=Animation(400, load_all_images("Resources/Animation/Player/idle/", (PLAYER_WIDTH, PLAYER_HEIGHT))),
        player_run=Animation(800, load_all_images("Resources/Animation/Player/run/", (PLAYER_WIDTH, PLAYER_HEIGHT))),
    )