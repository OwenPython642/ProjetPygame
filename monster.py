import pygame
import random
import animation


class Monster(animation.AnimateSprite):
    def __init__(self, game, name: str, size: tuple, offset: int = 0, animation_speed=1) -> None:
        super().__init__(name, size, animation_speed=animation_speed)
        self.game = game
        self.health: int = 100
        self.max_health: int = 100
        self.attack: float = 0.6
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset
        self.loot_amount: int = 10

    def set_loot_amount(self, amount: int) -> None:
        self.loot_amount = amount

    def set_speed(self, speed: int) -> None:
        self.default_speed = speed
        self.velocity = random.randint(1, speed)

    def damage(self, amount: int) -> None:
        self.health -= amount

        if self.health <= 0:
            self.health = self.max_health
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.game.add_score(self.loot_amount)
            if self.game.comet_event.is_full_loaded():
                self.game.all_monsters.remove(self)
                self.game.comet_event.attempt_fall()

    def update_animation(self) -> None:
        self.animation = True
        self.animate(loop=True)

    def update_health_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            (60, 63, 60),
            [self.rect.x + 10, self.rect.y - 20, self.max_health, 5],
        )
        pygame.draw.rect(
            surface,
            (111, 210, 46),
            [self.rect.x + 10, self.rect.y - 20, self.health, 5],
        )

    def forward(self) -> None:
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)


class Mummy(Monster):
    def __init__(self, game) -> None:
        self.size: tuple = (130, 130)
        self.offset: int = 0
        super().__init__(game, "mummy", self.size, self.offset)
        self.set_speed(3)
        self.set_loot_amount(20)


class Alien(Monster):
    def __init__(self, game) -> None:
        self.size: tuple = (300, 300)
        self.offset: int = 130
        super().__init__(game, "alien", self.size, self.offset)
        self.health: int = 250
        self.max_health: int = 250
        self.attack: float = 0.8
        self.set_speed(1)
        self.set_loot_amount(80)
