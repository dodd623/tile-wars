import pygame


class Renderer:
    def __init__(self, screen, tile_size=60):
        self.screen = screen
        self.tile_size = tile_size

        self.colors = {
            "background": (30, 30, 30),
            "grid": (80, 80, 80),
            "neutral": (50, 50, 50),
            "player": (70, 130, 180),
            "ai": (180, 70, 70),
            "text": (240, 240, 240),
            "selected": (255, 255, 0),
            "panel": (20, 20, 20),
            "accent": (200, 200, 200),
        }

        pygame.font.init()
        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 24, bold=True)
        self.font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 16)

    def draw(self, game_state):
        if game_state.game_phase == "start":
            self.draw_start_screen()
        elif game_state.game_phase == "playing":
            self.draw_game(game_state)
        elif game_state.game_phase == "game_over":
            self.draw_game_over(game_state)

        pygame.display.flip()

    def draw_game(self, game_state):
        self.screen.fill(self.colors["background"])

        for row in game_state.grid.tiles:
            for tile in row:
                self.draw_tile(tile, game_state.selected_tile)

    def draw_tile(self, tile, selected_tile=None):
        x = tile.x * self.tile_size
        y = tile.y * self.tile_size
        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

        if tile.owner == 0:
            color = self.colors["player"]
        elif tile.owner == 1:
            color = self.colors["ai"]
        else:
            color = self.colors["neutral"]

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.colors["grid"], rect, 2)

        if selected_tile and tile.x == selected_tile.x and tile.y == selected_tile.y:
            pygame.draw.rect(self.screen, self.colors["selected"], rect, 4)

        if tile.units > 0:
            text_surface = self.font.render(str(tile.units), True, self.colors["text"])
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def draw_start_screen(self):
        self.screen.fill(self.colors["background"])

        width, height = self.screen.get_size()

        title = self.title_font.render("Silent Front", True, self.colors["text"])
        title_rect = title.get_rect(center=(width // 2, 90))
        self.screen.blit(title, title_rect)

        subtitle = self.subtitle_font.render("Fogless prototype build", True, self.colors["accent"])
        subtitle_rect = subtitle.get_rect(center=(width // 2, 135))
        self.screen.blit(subtitle, subtitle_rect)

        info_lines = [
            "A grid-based strategy game inspired by Risk and Battleship.",
            "",
            "Objective:",
            "Expand your territory, manage your units, and eliminate the enemy force.",
            "",
            "How to play:",
            "- Click your tile to select it.",
            "- Click an adjacent empty tile to expand.",
            "- Click an adjacent enemy tile to attack.",
            "- Click an adjacent friendly tile to reinforce it.",
            "",
            "Current prototype goal:",
            "Build the core gameplay loop before adding smarter AI, fog of war, and endgame screens.",
            "",
            "Press SPACE to start.",
        ]

        start_y = 210
        for i, line in enumerate(info_lines):
            font = self.font if i not in [2, 6, 12] else self.subtitle_font
            rendered = font.render(line, True, self.colors["text"])
            rect = rendered.get_rect(center=(width // 2, start_y + i * 30))
            self.screen.blit(rendered, rect)

    def draw_game_over(self, game_state):
        self.screen.fill(self.colors["background"])

        width, height = self.screen.get_size()

        title = self.title_font.render("Game Over", True, self.colors["text"])
        title_rect = title.get_rect(center=(width // 2, height // 2 - 40))
        self.screen.blit(title, title_rect)

        winner_text = f"Winner: {'Player' if game_state.winner == 0 else 'AI'}"
        winner_surface = self.subtitle_font.render(winner_text, True, self.colors["text"])
        winner_rect = winner_surface.get_rect(center=(width // 2, height // 2 + 10))
        self.screen.blit(winner_surface, winner_rect)

        prompt = self.font.render("Close the window for now. Restart flow comes next.", True, self.colors["accent"])
        prompt_rect = prompt.get_rect(center=(width // 2, height // 2 + 60))
        self.screen.blit(prompt, prompt_rect)