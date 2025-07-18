import pygame
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, size=(200, 200), animation_speed=60) -> None:
        super().__init__()
        self.size = size
        self.current_image: int = 0
        result = animation.get(sprite_name)
        if result is None:
            raise ValueError(f"Aucune animation trouvée pour '{sprite_name}'")
        # Scale images once on load
        self.images = [pygame.transform.scale(img, self.size) for img in result]
        self.image = self.images[0]
        self.animation: bool = False
        self.last_update_time = time.time()
        self.animation_speed = animation_speed  # seconds per frame

    def start_animation(self) -> None:
        self.animation = True
        self.last_update_time = time.time()

    def animate(self, loop=True) -> None:
        if not self.animation:
            return

        current_time = time.time()
        if current_time - self.last_update_time > self.animation_speed:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
                if not loop:
                    self.animation = False
            self.image = self.images[self.current_image]
            self.last_update_time = current_time


def load_animation_images(sprite_name) -> list[pygame.surface.Surface]:
    images: list = []
    path = (
        os.path.join(ASSETS_DIR, rf"{sprite_name}\{sprite_name}")
    )
    for num in range(1, 24):
        image_path = path + str(num) + ".png"
        images.append(pygame.image.load(image_path))

    return images


animation = {
    "mummy": load_animation_images("mummy"),
    "player": load_animation_images("player"),
    "alien": load_animation_images("alien"),
}
