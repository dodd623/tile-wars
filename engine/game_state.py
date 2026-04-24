from engine.grid import Grid
from mechanics.combat import resolve_capture
from players.player_profile import create_player_profiles, DEFAULT_PLAYER_COLORS


class GameState:
    def __init__(self, num_players=2, human_players=1, domination_threshold=0.6):
        self.game_phase = "setup"

        self.num_players = num_players
        self.human_players = human_players
        self.domination_threshold = domination_threshold

        self.grid_size_options = [(10, 10), (12, 12), (15, 15), (20, 20)]
        self.grid_size_index = 0
        self.grid_width, self.grid_height = self.grid_size_options[self.grid_size_index]

        self.selected_setup_player = 0
        self.players = create_player_profiles(num_players, human_players)

        self.grid = None
        self.current_player = 0
        self.selected_tile = None
        self.winner = None
        self.eliminated_players = set()

        self.turn_count = 0
        self.max_turns = self.grid_width * self.grid_height * 6
        self.event_log = []

    def calculate_max_turns(self):
        return self.grid_width * self.grid_height * 4

    def rebuild_players(self):
        old_players = self.players
        new_players = create_player_profiles(self.num_players, self.human_players)

        for player_id, new_profile in new_players.items():
            if player_id in old_players:
                old_profile = old_players[player_id]

                new_profile["name"] = old_profile["name"]
                new_profile["color"] = old_profile["color"]
                new_profile["color_name"] = old_profile["color_name"]
                new_profile["color_index"] = old_profile["color_index"]

        self.players = new_players

        if self.selected_setup_player >= self.num_players:
            self.selected_setup_player = self.num_players - 1

    def increase_total_players(self):
        if self.num_players < 8:
            self.num_players += 1
            self.rebuild_players()

    def decrease_total_players(self):
        if self.num_players > 1:
            self.num_players -= 1

            if self.human_players > self.num_players:
                self.human_players = self.num_players

            self.rebuild_players()

    def increase_human_players(self):
        if self.human_players < self.num_players:
            self.human_players += 1
            self.rebuild_players()

    def decrease_human_players(self):
        if self.human_players > 0:
            self.human_players -= 1
            self.rebuild_players()

    def cycle_grid_size(self):
        self.grid_size_index = (self.grid_size_index + 1) % len(self.grid_size_options)
        self.grid_width, self.grid_height = self.grid_size_options[self.grid_size_index]
        self.max_turns = self.calculate_max_turns()

    def next_setup_player(self):
        self.selected_setup_player = (self.selected_setup_player + 1) % self.num_players

    def cycle_selected_player_color(self):
        profile = self.players[self.selected_setup_player]

        new_index = (profile["color_index"] + 1) % len(DEFAULT_PLAYER_COLORS)
        color_data = DEFAULT_PLAYER_COLORS[new_index]

        profile["color_index"] = new_index
        profile["color"] = color_data["value"]
        profile["color_name"] = color_data["name"]

    def rename_selected_player(self, new_name):
        cleaned_name = new_name.strip()

        if cleaned_name:
            self.players[self.selected_setup_player]["name"] = cleaned_name

    def start_game(self):
        self.grid = Grid(width=self.grid_width, height=self.grid_height)
        self.grid.initialize_players(num_players=self.num_players)

        self.current_player = 0
        self.selected_tile = None
        self.winner = None
        self.eliminated_players = set()
        self.turn_count = 1
        self.max_turns = self.calculate_max_turns()
        self.event_log = [f"Match started. Turn limit: {self.max_turns}."]

        self.game_phase = "playing"

    def restart_game(self):
        self.start_game()

    def return_to_setup(self):
        self.grid = None
        self.current_player = 0
        self.selected_tile = None
        self.winner = None
        self.eliminated_players = set()
        self.turn_count = 0
        self.max_turns = self.calculate_max_turns()
        self.event_log = []
        self.game_phase = "setup"

    def switch_turn(self):
        self.selected_tile = None
        self.update_eliminated_players()

        if len(self.eliminated_players) >= self.num_players - 1:
            for player_id in range(self.num_players):
                if player_id not in self.eliminated_players:
                    self.winner = player_id
                    self.game_phase = "game_over"
                    return

        while True:
            self.current_player = (self.current_player + 1) % self.num_players

            if self.current_player not in self.eliminated_players:
                break

        self.turn_count += 1
        self.check_stalemate_victory()

    def get_current_player(self):
        return self.current_player

    def is_human_turn(self):
        return (
            self.current_player not in self.eliminated_players
            and self.players[self.current_player]["type"] == "human"
        )

    def is_ai_turn(self):
        return (
            self.current_player not in self.eliminated_players
            and self.players[self.current_player]["type"] == "ai"
        )

    def get_current_player_profile(self):
        return self.players[self.current_player]

    def handle_player_click(self, tile):
        if tile is None or self.game_phase != "playing":
            return

        if self.selected_tile is None:
            if tile.owner == self.current_player:
                self.selected_tile = tile
            return

        if tile == self.selected_tile:
            self.selected_tile = None
            return

        if self.selected_tile.owner != self.current_player:
            self.selected_tile = None
            return

        neighbors = self.grid.get_neighbors(self.selected_tile.x, self.selected_tile.y)

        if tile not in neighbors:
            self.selected_tile = None
            return

        if tile.owner == self.current_player:
            self.selected_tile = tile
            return

        self.resolve_move(self.selected_tile, tile)
        self.selected_tile = None

    def resolve_move(self, source_tile, target_tile):
        if source_tile.owner != self.current_player:
            return

        attacker_id = source_tile.owner
        defender_id = target_tile.owner

        captured = resolve_capture(source_tile, target_tile)

        if defender_id is None and captured:
            self.add_event(f"{self.players[attacker_id]['name']} expanded.")

        elif defender_id is not None and defender_id != attacker_id:
            if captured:
                attacker_name = self.players[attacker_id]["name"]
                defender_name = self.players[defender_id]["name"]
                self.add_event(f"{attacker_name} captured territory from {defender_name}.")
            else:
                self.add_event(f"{self.players[attacker_id]['name']} failed to capture.")

        self.update_eliminated_players()
        self.check_domination_victory()

        if self.game_phase != "game_over":
            self.switch_turn()

    def add_event(self, message):
        self.event_log.insert(0, message)
        self.event_log = self.event_log[:6]

    def get_selectable_tiles(self):
        selectable_tiles = []

        if self.game_phase != "playing":
            return selectable_tiles

        for row in self.grid.tiles:
            for tile in row:
                if tile.owner != self.current_player:
                    continue

                neighbors = self.grid.get_neighbors(tile.x, tile.y)

                has_valid_target = any(
                    neighbor.owner != self.current_player
                    for neighbor in neighbors
                )

                if has_valid_target:
                    selectable_tiles.append(tile)

        return selectable_tiles

    def get_valid_target_tiles(self):
        if self.selected_tile is None:
            return []

        if self.selected_tile.owner != self.current_player:
            return []

        neighbors = self.grid.get_neighbors(self.selected_tile.x, self.selected_tile.y)

        return [
            neighbor
            for neighbor in neighbors
            if neighbor.owner != self.current_player
        ]

    def update_eliminated_players(self):
        if self.grid is None:
            return

        owned_counts = self.grid.count_owned_tiles()

        for player_id in range(self.num_players):
            if owned_counts.get(player_id, 0) == 0:
                if player_id not in self.eliminated_players:
                    self.add_event(f"{self.players[player_id]['name']} was eliminated.")
                self.eliminated_players.add(player_id)

    def check_domination_victory(self):
        owned_counts = self.grid.count_owned_tiles()
        required_tiles = int(self.grid.total_tiles() * self.domination_threshold)

        for player_id, count in owned_counts.items():
            if count >= required_tiles:
                self.winner = player_id
                self.game_phase = "game_over"
                self.add_event(f"{self.players[player_id]['name']} won by domination.")
                return

        active_players = [
            player_id
            for player_id in range(self.num_players)
            if player_id not in self.eliminated_players
        ]

        if len(active_players) == 1:
            self.winner = active_players[0]
            self.game_phase = "game_over"
            self.add_event(f"{self.players[self.winner]['name']} is the last player standing.")

    def check_stalemate_victory(self):
        if self.turn_count < self.max_turns:
            return

        owned_counts = self.grid.count_owned_tiles()

        active_counts = {
            player_id: count
            for player_id, count in owned_counts.items()
            if player_id not in self.eliminated_players
        }

        if not active_counts:
            return

        self.winner = max(active_counts, key=active_counts.get)
        self.game_phase = "game_over"
        self.add_event(
            f"Turn limit reached. {self.players[self.winner]['name']} wins by territory."
        )