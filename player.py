import pygame
from projectile import Projectile
import animation


class Player(animation.AnimateSprite):
    def __init__(self, game, animation_speed=1) -> None:
        self.size = (200, 200)
        super().__init__("player", self.size, animation_speed=animation_speed)
        self.game = game
        self.health: int = 100
        self.max_health: int = 100
        self.attack: int = 10
        self.velocity: int = 5
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def damage(self, amount: int) -> None:
        if self.health - amount > 0:
            self.health -= amount
        else:
            self.game.game_over()

    def update_animation(self) -> None:
        self.animate(loop=False)

    def update_health_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            (60, 63, 60),
            [self.rect.x + 50, self.rect.y + 20, self.max_health, 5],
        )
        pygame.draw.rect(
            surface,
            (111, 210, 46),
            [self.rect.x + 50, self.rect.y + 20, self.health, 5],
        )

    def launch_projectile(self) -> None:
        self.all_projectiles.add(Projectile(self))
        self.animation = True
        self.start_animation()
        self.game.sound_manager.play("tir")

    def move_right(self) -> None:
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self) -> None:
        self.rect.x -= self.velocity
