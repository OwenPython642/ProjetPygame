import pygame
from comet import Comet


class CometFallEvent:
    def __init__(self, game) -> None:
        self.percent: float = 0
        self.percent_speed: int = 10
        self.all_comets = pygame.sprite.Group()
        self.game = game
        self.fall_mode: bool = False

    def add_percent(self) -> None:
        self.percent += self.percent_speed / 100

    def is_full_loaded(self) -> float:
        return self.percent >= 100

    def reset_percent(self) -> None:
        self.percent: float = 0

    def meteor_fall(self) -> None:
        for _ in range(1, 23):
            self.all_comets.add(Comet(self))
        self.game.wave += 1

    def attempt_fall(self) -> None:
        if (
            self.is_full_loaded()
            and len(self.game.all_monsters) == 0
            and not self.fall_mode
        ):
            self.meteor_fall()

            self.fall_mode: bool = True

    def update_bar(self, surface: pygame.Surface) -> None:

        self.add_percent()

        self.attempt_fall()

        pygame.draw.rect(
            surface, (0, 0, 0), [0, surface.get_height() - 20, surface.get_width(), 10]
        )
        pygame.draw.rect(
            surface,
            (187, 11, 11),
            [
                0,
                surface.get_height() - 20,
                (surface.get_width() / 100) * self.percent,
                10,
            ],
        )
