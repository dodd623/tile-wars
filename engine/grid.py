class Tile:
    def __init__(self, x, y, owner=None):
        self.x = x
        self.y = y
        self.owner = owner

    def __repr__(self):
        return f"Tile({self.x}, {self.y}, owner={self.owner})"


class Grid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.tiles = [
            [Tile(x, y) for x in range(width)]
            for y in range(height)
        ]

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def get_neighbors(self, x, y):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        neighbors = []

        for dx, dy in directions:
            neighbor = self.get_tile(x + dx, y + dy)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def initialize_players(self, num_players=2):
        starting_positions = [
            (0, 0),
            (self.width - 1, self.height - 1),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width // 2, 0),
            (self.width // 2, self.height - 1),
            (0, self.height // 2),
            (self.width - 1, self.height // 2),
        ]

        for player_id in range(num_players):
            x, y = starting_positions[player_id]
            tile = self.get_tile(x, y)
            tile.owner = player_id

    def count_owned_tiles(self):
        tile_counts = {}

        for row in self.tiles:
            for tile in row:
                if tile.owner is not None:
                    tile_counts[tile.owner] = tile_counts.get(tile.owner, 0) + 1

        return tile_counts

    def total_tiles(self):
        return self.width * self.height