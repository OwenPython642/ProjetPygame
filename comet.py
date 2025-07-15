import pygame
import random

_comet_image = pygame.image.load(
    r"C:\Users\owenp\Desktop\pythontest\pygame\assets\comet.png"
)


class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_event) -> None:
        super().__init__()
        self.attack: int = 20
        self.comet_event = comet_event
        self.image = _comet_image
        self.rect = self.image.get_rect()
        self.velocity: int = random.randint(6, 9)
        self.rect.x = random.randint(20, 1000)
        self.rect.y = -random.randint(0, 1000)

    def remove(self) -> None:
        self.comet_event.all_comets.remove(self)

        self.comet_event.game.sound_manager.play("meteorite")

        if len(self.comet_event.all_comets) == 0:
            self.comet_event.reset_percent()
            self.comet_event.game.start()

    def fall(self) -> None:
        self.rect.y += self.velocity

        if self.rect.y >= 500:
            self.remove()

            if len(self.comet_event.all_comets) == 0:
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False

        if self.comet_event.game.check_collision(
            self, self.comet_event.game.all_players
        ):
            self.comet_event.game.player.damage(self.attack)
            self.remove()
