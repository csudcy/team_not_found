import random

from team_not_found.games.tanks import external


class Team(external.ExternalTeam):
    #Give the team a nice name
    name = 'Passive (Runner-Random)'

    def init_players(self, PlayerClass, board_width, board_height, min_x, max_x, min_y, max_y, enemy_direction):
        #Need these later...
        self.board_width = board_width
        self.board_height = board_height

        #Initialise the players
        players = []
        x = (min_x + max_x) / 2
        y_step = (max_y - min_y) / 4
        for i in xrange(5):
            player = PlayerClass(
                x=x,
                y=min_y + i * y_step,
                direction=enemy_direction,
                turret_direction=enemy_direction,
                speed=25,
                sight=25,
                health=25,
                blast_radius=25,
            )
            self.set_random_target(player)
            players.append(player)
        return players

    def set_random_target(self, player):
        player.set_target(
            random.randint(0, self.board_width),
            random.randint(0, self.board_height),
        )

    def run_tick(self, live_players, seen):
        for player in live_players:
            #We want to move around
            if player.in_target:
                self.set_random_target(player)
