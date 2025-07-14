import pygame
from game import Game
import math

import os

pygame.init()

FPS = 60

pygame.display.set_caption("Comet Fall Game")

game = Game()

# Use relative paths for assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

background = pygame.image.load(os.path.join(ASSETS_DIR, "bg.jpg"))

play_button = pygame.image.load(os.path.join(ASSETS_DIR, "button.png"))
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(game.screen.get_width() / 3.33)
play_button_rect.y = math.ceil(game.screen.get_height() / 2)


def run() -> None:
    clock = pygame.time.Clock()
    
    running = True

    while running:
        game.screen.blit(background, (0, -200))

        if game.is_playing:
            game.update(game.screen)
        else:
            game.screen.blit(play_button, play_button_rect)
            game.screen.blit(game.banner, game.banner_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_SPACE:
                    game.player.launch_projectile()
                elif event.key == pygame.K_ESCAPE:
                    # Proper toggle for pause
                    game.is_paused = not game.is_paused
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game.start()
                    game.sound_manager.play("click")
        clock.tick(FPS)


if __name__ == "__main__":
    run()
