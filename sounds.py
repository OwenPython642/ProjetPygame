import pygame


class SoundManager:
    def __init__(self) -> None:
        self.sounds: dict = {
            "click": pygame.mixer.Sound(
                r"C:\Users\owenp\Desktop\pythontest\pygame\assets\sounds\click.ogg"
            ),
            "game_over": pygame.mixer.Sound(
                r"C:\Users\owenp\Desktop\pythontest\pygame\assets\sounds\game_over.ogg"
            ),
            "meteorite": pygame.mixer.Sound(
                r"C:\Users\owenp\Desktop\pythontest\pygame\assets\sounds\meteorite.ogg"
            ),
            "tir": pygame.mixer.Sound(
                r"C:\Users\owenp\Desktop\pythontest\pygame\assets\sounds\tir.ogg"
            ),
        }
        for sound in self.sounds.values():
            sound.set_volume(0.1)  # Set volume once during initialization

    def play(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound:
            sound.play()
