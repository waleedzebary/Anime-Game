class Settings:
    def __init__(self):
        self.speed = 1.0
        self.bullets_allowed = 10
        self.screen_width = 1550
        self.speed = 1.5
        self.screen_height = 800
        self.fleet_drop_speed = 10
        self.fleet_dir = 1
        self.player_limit = 2
        self.speed_up = 1.1
        self.score_scale = 1.5
        self.bg_color = (0, 0, 0)
        self.initialize_dynamic_sittings()

    def initialize_dynamic_sittings(self):
        self.player_speed = 1.5
        self.bullet_speed = 1
        self.enemies_speed = 1
        self.fleet_dir = 1
        self.enemies_point= 5

    def increase_speed(self):
        self.player_speed *= self.speed_up
        self.bullet_speed *= self.speed_up
        self.enemies_speed *= self.speed_up
        self.enemies_point = int(self.enemies_point * self.score_scale)
