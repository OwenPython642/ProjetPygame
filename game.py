import pygame
from player import Player
from monster import Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager


class Game:
    def __init__(self) -> None:
        self.is_playing: bool = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.comet_event = CometFallEvent(self)
        self.all_monsters = pygame.sprite.Group()
        self.sound_manager = SoundManager()
        self.font = pygame.font.Font(
            r"C:\Users\owenp\Desktop\pythontest\pygame\assets\arial.ttf", 16
        )
        self.score: int = 0
        self.pressed: dict = {}

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(
            sprite, group, False, pygame.sprite.collide_mask
        )

    def spawn_monster(self, monster_class_name) -> None:
        self.all_monsters.add(monster_class_name(self))

    def start(self) -> None:
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def add_score(self, amount=20) -> None:
        self.score += amount

    def game_over(self) -> None:
        self.comet_event.all_comets = pygame.sprite.Group()
        self.is_playing = False
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.score = 0
        self.sound_manager.play("game_over")

    def update(self, screen: pygame.Surface) -> None:

        score_text = self.font.render(f"score: {self.score}", 1, (0, 0, 0))

        screen.blit(self.player.image, self.player.rect)

        screen.blit(score_text, (20, 20))

        self.player.update_health_bar(screen)
        self.player.update_animation()

        self.comet_event.update_bar(screen)

        for projectile in self.player.all_projectiles:
            projectile.move()

        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        for comet in self.comet_event.all_comets:
            comet.fall()

        self.player.all_projectiles.update()
        self.player.all_projectiles.draw(screen)

        self.all_monsters.update()
        self.all_monsters.draw(screen)

        self.comet_event.all_comets.update()
        self.comet_event.all_comets.draw(screen)

        if (
            self.pressed.get(pygame.K_RIGHT)
            and self.player.rect.x + self.player.rect.width < screen.get_width()
        ):
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
