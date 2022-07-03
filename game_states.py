class GameStats:
    def __init__(self, sj_game):
        self.settings = sj_game.settings
        self.reset_stats()
        self.game_active = True
        self.high_score = 0

    def reset_stats(self):
        self.player_left = self.settings.player_limit
        self.score = 0
