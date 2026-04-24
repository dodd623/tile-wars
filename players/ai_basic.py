import random


class BasicAI:
    def __init__(self, player_id=1):
        self.player_id = player_id

    def take_turn(self, game_state):
        owned_tiles = self.get_owned_tiles(game_state)

        if not owned_tiles:
            game_state.switch_turn()
            return

        all_moves = self.get_all_legal_moves(game_state, owned_tiles)

        if not all_moves:
            game_state.switch_turn()
            return

        source_tile, target_tile = self.choose_move(game_state, all_moves)
        game_state.resolve_move(source_tile, target_tile)

    def choose_move(self, game_state, all_moves):
        kill_moves = []
        attack_moves = []
        expand_moves = []

        owned_counts = game_state.grid.count_owned_tiles()

        for source_tile, target_tile in all_moves:
            if target_tile.owner is None:
                expand_moves.append((source_tile, target_tile))

            elif target_tile.owner != self.player_id:
                target_owner = target_tile.owner
                would_eliminate = owned_counts.get(target_owner, 0) == 1

                if would_eliminate:
                    kill_moves.append((source_tile, target_tile))
                else:
                    attack_moves.append((source_tile, target_tile))

        if kill_moves:
            return random.choice(kill_moves)

        if attack_moves and random.random() < 0.65:
            return random.choice(attack_moves)

        if expand_moves and random.random() < 0.85:
            return random.choice(expand_moves)

        return random.choice(all_moves)

    def get_all_legal_moves(self, game_state, owned_tiles):
        moves = []

        for source_tile in owned_tiles:
            neighbors = game_state.grid.get_neighbors(source_tile.x, source_tile.y)

            for target_tile in neighbors:
                if target_tile.owner != self.player_id:
                    moves.append((source_tile, target_tile))

        random.shuffle(moves)
        return moves

    def get_owned_tiles(self, game_state):
        owned_tiles = []

        for row in game_state.grid.tiles:
            for tile in row:
                if tile.owner == self.player_id:
                    owned_tiles.append(tile)

        random.shuffle(owned_tiles)
        return owned_tiles