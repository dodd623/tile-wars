class Tile:
    def __init__(self, x, y, owner=None, units=0):
        self.x = x
        self.y = y
        self.owner = owner  # None, 0 (player), 1 (AI)
        self.units = units

    def __repr__(self):
        return f"Tile({self.x}, {self.y}, owner={self.owner}, units={self.units})"


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
        directions = [
            (0, -1),  # up
            (0, 1),   # down
            (-1, 0),  # left
            (1, 0),   # right
        ]

        neighbors = []
        for dx, dy in directions:
            neighbor = self.get_tile(x + dx, y + dy)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def initialize_players(self):
        # Player 0 (human)
        self.get_tile(0, 0).owner = 0
        self.get_tile(0, 0).units = 5

        # Player 1 (AI)
        self.get_tile(self.width - 1, self.height - 1).owner = 1
        self.get_tile(self.width - 1, self.height - 1).units = 5