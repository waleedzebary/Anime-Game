import sys
import pygame
import time
from settings import Settings
from background import Background
from player import Player
from pygame import mixer
from bullet import Bullet
from enemy import Enemie
from game_states import GameStats
from scoreboard import Scoreboard


class AnimeGame:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # pygame.display.set_icon(img)
        self.player = Player(self)
        self.bullet = pygame.sprite.Group()
        self.bullet_image = Bullet(self)
        self.enemies = pygame.sprite.Group()
        self._create_fleet()
        self.screen_rect = self.screen.get_rect()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        pygame.display.set_caption("anime game")
        self.background = Background(self)

    def run_game(self):
        while True:
            self._check_events()
            self.background.update()
            if self.stats.game_active:
                self.player.update()
                # self.update_bullet()
                self.bullet.update()
                self.update_enemies()
            self.screen.blit(self.background.image, (0, 0))
            self.screen.blit(self.player.playerImage, self.player.rect)
            self.bullet_remove()
            self.update_screen()
            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_w:
            self.player.moving_top = True
        elif event.key == pygame.K_s:
            self.player.moving_down = True
        elif event.key == pygame.K_d:
            self.player.moving_foreword = True
            # self.bullet_image.fireMe = False
        elif event.key == pygame.K_a:
            self.player.moving_backward = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_w:
            self.player.moving_top = False
        elif event.key == pygame.K_s:
            self.player.moving_down = False
        elif event.key == pygame.K_d:
            self.player.moving_foreword = False
        elif event.key == pygame.K_a:
            self.player.moving_backward = False
        # elif event.key == pygame.K_SPACE:
        #     pass

    def _fire_bullet(self):
        if len(self.bullet) < self.settings.bullets_allowed:
            self.bullet_image.bullet_sound()
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

    def bullet_remove(self):
        self.bullet.update()
        for bullet in self.bullet.copy():
            if bullet.rect.left >= self.screen.get_width() or bullet.rect.right <= 0:
                self.bullet.remove(bullet)
        self._check_bullet_hit_enemie()
        # print("hi")

    def _check_bullet_hit_enemie(self):
        collisions = pygame.sprite.groupcollide(self.bullet, self.enemies, True, True)
        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemies_speed * len(enemies)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.enemies:
            self.bullet.empty()
            self._create_fleet()
            self.settings.increase_speed()
        print(len(self.bullet))

    def update_screen(self):
        self.bullet.update()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.enemies.draw(self.screen)
        self.sb.show_score()
        pygame.display.flip()
        pygame.display.update()

    def _create_fleet(self):
        enemie = Enemie(self)
        enemie_width, enemie_height = enemie.rect.size
        a_space_x = self.settings.screen_width - (2 * enemie_width)
        num_enemie_x = a_space_x // (2 * enemie_width)
        ship_height = self.player.rect.height
        a_space_y = (self.settings.screen_height - (4 + enemie_height) - ship_height)
        num_rows = a_space_y // (2 * enemie_height)
        for row_num in range(num_rows):
            for enemie_nume in range(num_enemie_x):
                self._create_eneime(enemie_nume, row_num)

    def _create_eneime(self, enemie1_num, row_num):
        enemie1 = Enemie(self)
        enemie1_width, enemie1_height = enemie1.rect.size
        enemie1.rect.x = enemie1.rect.width + 1.5 * enemie1.rect.width * row_num
        enemie1.rect.y = enemie1.y
        enemie1.y = enemie1_height + 1 * enemie1_height * enemie1_num
        enemie1.rect.x = enemie1.x
        self.enemies.add(enemie1)

    def update_enemies(self):
        self.check_fleet_edges()
        self.enemies.update()
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player_hit()
        self.check_enemy_left()

    def check_fleet_edges(self):
        for enemies in self.enemies.sprites():
            if enemies.check_edges():
                self._change_fleet_dir()
                break

    def _change_fleet_dir(self):
        for eneime in self.enemies.sprites():
            eneime.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_dir *= -1

    def player_hit(self):
        if self.stats.player_left > 0:
            self.stats.player_left -= 1
            self.sb.prep_players()
            self.enemies.empty()
            self.bullet.empty()
            self._create_fleet()
            self.player.center_ship()
            time.sleep(0.5)
            self.sb.prep_score()
        else:
            self.stats.game_active = False

    def update_bullet(self):
        for bullets in self.bullet.copy():
            if bullets.rect.bottom <= 0:
                self.bullet.remove(bullets)
        self._check_bullet_hit_enemie()

    def check_enemy_left(self):
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.left == screen_rect.left:
                self.player_hit()
                break


if __name__ == '__main__':
    ag = AnimeGame()
    ag.run_game()

