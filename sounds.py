import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets/sounds")

class SoundManager:
    def __init__(self) -> None:
        self.sounds: dict = {
            "click": pygame.mixer.Sound(
                os.path.join(ASSETS_DIR, "click.ogg")
            ),
            "game_over": pygame.mixer.Sound(
                os.path.join(ASSETS_DIR, "game_over.ogg")
            ),
            "meteorite": pygame.mixer.Sound(
                os.path.join(ASSETS_DIR, "meteorite.ogg")
            ),
            "tir": pygame.mixer.Sound(
                os.path.join(ASSETS_DIR, "tir.ogg")
            ),
        }
        for sound in self.sounds.values():
            sound.set_volume(0.1)  # Set volume once during initialization

    def play(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound:
            sound.play()
