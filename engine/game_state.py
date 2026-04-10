from engine.grid import Grid
from mechanics.combat import resolve_combat


class GameState:
    def __init__(self):
        self.game_phase = "start"  # start, playing, game_over

        self.grid = Grid()
        self.grid.initialize_players()

        self.current_player = 0
        self.num_players = 2
        self.selected_tile = None

        self.winner = None

    def start_game(self):
        self.game_phase = "playing"

    def switch_turn(self):
        self.current_player = (self.current_player + 1) % self.num_players

    def get_current_player(self):
        return self.current_player

    def is_player_turn(self):
        return self.current_player == 0

    def is_ai_turn(self):
        return self.current_player == 1

    def handle_player_click(self, tile):
        if tile is None or self.game_phase != "playing":
            return

        if self.selected_tile is None:
            if tile.owner == 0:
                self.selected_tile = tile
            return

        if tile.x == self.selected_tile.x and tile.y == self.selected_tile.y:
            self.selected_tile = None
            return

        neighbors = self.grid.get_neighbors(self.selected_tile.x, self.selected_tile.y)
        if tile not in neighbors:
            return

        if self.selected_tile.units <= 1:
            self.selected_tile = None
            return

        if tile.owner is None:
            tile.owner = self.selected_tile.owner
            tile.units = self.selected_tile.units - 1
            self.selected_tile.units = 1

        elif tile.owner != self.selected_tile.owner:
            resolve_combat(self.selected_tile, tile)

        else:
            tile.units += self.selected_tile.units - 1
            self.selected_tile.units = 1

        self.selected_tile = None
        self.switch_turn()