from Settings import *
from os import listdir

# Constants
ALLOWED_FILES = ("png", "jpg", "jpeg", "webp")


def load_all_images(dir_path, size):
    paths = listdir(dir_path)
    all_images = []
    for path in paths:
        if path.split(".")[-1] in ALLOWED_FILES:
            py.transform.scale(py.image.load(dir_path + path), size)

    return all_images


class Animator:
    def __init__(self, **kwargs):
        self.anim = dict(kwargs)


class Animation:
    def __init__(self, duration: float, *images):
        self.duration = duration
        self.images = list(images)


if __name__ == '__main__':
    ANIMATOR = Animator(
        player_idle=Animation(1, load_all_images("Resources/Animation/Player/idle/", (PLAYER_WIDTH, PLAYER_HEIGHT))),
        player_run=Animation(1, load_all_images("Resources/Animation/Player/run/", (PLAYER_WIDTH, PLAYER_HEIGHT))),
    )