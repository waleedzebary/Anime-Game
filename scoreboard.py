import pygame.font
from pygame.sprite import Group
from player import Player


class Scoreboard:
    def __init__(self, sj_game):
        self.sj_game = sj_game
        self.screen = sj_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sj_game.settings
        self.stats = sj_game.stats
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_players()

    def prep_players(self):
        self.players = Group()
        for player_number in range(self.stats.player_left):
            player = Player(self.sj_game)
            player.rect.x = 10 + player_number * player.rect.width
            player.rect.y = 10
            self.players.add(player)

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render('Score: ' + score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = str(self.stats.high_score)
        # high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render('High Score: ' + high_score, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # self.players.draw(self.screen)
