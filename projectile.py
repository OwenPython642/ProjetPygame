import pygame

_projectile_image = pygame.transform.scale(
    pygame.image.load(
        r"assets\projectile.png"
    ),
    (50, 50),
)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player) -> None:
        super().__init__()
        self.velocity: int = 5
        self.player = player
        self.image = _projectile_image
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle: int = 0

    def rotate(self) -> None:
        self.angle -= 2
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self) -> None:
        self.player.all_projectiles.remove(self)

    def move(self) -> None:
        self.rect.x += self.velocity
        self.rotate()

        for monster in self.player.game.check_collision(
            self, self.player.game.all_monsters
        ):
            monster.damage(self.player.attack)
            self.remove()

        if self.rect.x > 1080:
            self.remove()
