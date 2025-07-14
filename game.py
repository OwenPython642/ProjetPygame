import pygame
from player import Player
from monster import Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager
import math
import os


class Game:
    def __init__(self) -> None:
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.nb_escape = 0
        self.all_players = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((1080, 720))

        # Use relative paths for assets
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ASSETS_DIR = os.path.join(BASE_DIR, "assets")

        self.banner = pygame.image.load(os.path.join(ASSETS_DIR, "banner.png"))
        self.banner = pygame.transform.scale(self.banner, (500, 500))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = math.ceil(self.screen.get_width() / 4)
        # Set slower fixed animation speed for player and monsters
        animation_speed = 0

        self.player = Player(self, animation_speed=animation_speed)
        self.all_players.add(self.player)
        self.comet_event = CometFallEvent(self)
        self.all_monsters = pygame.sprite.Group()
        self.sound_manager = SoundManager()
        self.font = pygame.font.Font(os.path.join(ASSETS_DIR, "arial.ttf"), 16)
        self.score: int = 0
        self.pressed: dict = {}

    def pause_game(self, screen: pygame.Surface) -> None:
        self.screen.blit(self.banner, self.banner_rect)
        # Increase font size and make text bold for paused message
        bold_font = pygame.font.Font(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "arial.ttf"), 128)
        paused_text = bold_font.render("paused ...", True, (255, 255, 255))
        screen.blit(paused_text, (350, 500))

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(
            sprite, group, False, pygame.sprite.collide_mask
        )

    def spawn_monster(self, monster_class_name, count=1) -> None:
        for _ in range(count):
            self.all_monsters.add(monster_class_name(self))

    def start(self) -> None:
        self.is_playing = True
        self.spawn_monster(Mummy, 2)
        self.spawn_monster(Alien, 1)

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
        if not self.is_paused:
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

        if not self.is_paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.player.rect.x + self.player.rect.width < screen.get_width():
                self.player.move_right()
            elif keys[pygame.K_LEFT] and self.player.rect.x > 0:
                self.player.move_left()
        else:
            self.pause_game(screen)
