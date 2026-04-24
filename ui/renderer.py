import pygame


class Renderer:
    def __init__(self, screen, tile_size=40):
        self.screen = screen
        self.tile_size = tile_size
        self.sidebar_width = 360

        self.colors = {
            "background": (30, 30, 30),
            "grid": (80, 80, 80),
            "neutral": (50, 50, 50),
            "text": (240, 240, 240),
            "selected": (255, 255, 0),
            "accent": (200, 200, 200),
            "selectable": (120, 220, 255),
            "target": (255, 255, 255),
            "enemy_target": (255, 90, 90),
            "eliminated": (120, 120, 120),
            "panel": (20, 20, 20),
        }

        pygame.font.init()
        self.title_font = pygame.font.SysFont("arial", 42, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 24, bold=True)
        self.font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 16)

    def get_dynamic_tile_size(self, game_state):
        width, height = self.screen.get_size()

        usable_width = max(200, width - self.sidebar_width)
        usable_height = max(200, height)

        tile_width = usable_width // game_state.grid.width
        tile_height = usable_height // game_state.grid.height

        return max(12, min(tile_width, tile_height))

    def get_sidebar_x(self, game_state, tile_size):
        return game_state.grid.width * tile_size + 20

    def draw(self, game_state, editing_name=False, name_input="", paused=False, ai_delay=500):
        if game_state.game_phase == "setup":
            self.draw_setup_screen(game_state, editing_name, name_input)
        elif game_state.game_phase == "playing":
            self.draw_game(game_state, paused, ai_delay)
        elif game_state.game_phase == "game_over":
            self.draw_game(game_state, paused, ai_delay)
            self.draw_game_over_overlay(game_state)

        pygame.display.flip()

    def draw_setup_screen(self, game_state, editing_name=False, name_input=""):
        self.screen.fill(self.colors["background"])
        width, _ = self.screen.get_size()

        title = self.title_font.render("Silent Front Setup", True, self.colors["text"])
        self.screen.blit(title, title.get_rect(center=(width // 2, 60)))

        setup_lines = [
            f"Total Players: {game_state.num_players}",
            f"Human Players: {game_state.human_players}",
            f"AI Players: {game_state.num_players - game_state.human_players}",
            f"Grid Size: {game_state.grid_width}x{game_state.grid_height}",
            "",
            "Controls:",
            "UP/DOWN = change total players",
            "LEFT/RIGHT = change human player count",
            "G = cycle grid size",
            "TAB = select player profile",
            "C = cycle selected player color",
            "N = rename selected player",
            "SPACE = start match",
        ]

        y = 125
        for line in setup_lines:
            rendered = self.font.render(line, True, self.colors["text"])
            self.screen.blit(rendered, (60, y))
            y += 30

        self.draw_setup_player_list(game_state)

        if editing_name:
            edit_text = self.subtitle_font.render(
                f"Editing Name: {name_input}_",
                True,
                self.colors["selected"],
            )
            self.screen.blit(edit_text, (60, 580))

    def draw_setup_player_list(self, game_state):
        start_x = 460
        start_y = 125

        title = self.subtitle_font.render("Players", True, self.colors["text"])
        self.screen.blit(title, (start_x, start_y))

        for player_id, profile in game_state.players.items():
            y = start_y + 45 + player_id * 38

            marker = ">" if player_id == game_state.selected_setup_player else " "

            color_box = pygame.Rect(start_x + 30, y + 4, 18, 18)
            pygame.draw.rect(self.screen, profile["color"], color_box)

            label = (
                f"{marker} {profile['name']} | "
                f"{profile['type'].upper()} | "
                f"{profile['color_name']}"
            )

            text = self.font.render(label, True, self.colors["text"])
            self.screen.blit(text, (start_x + 60, y))

    def draw_game(self, game_state, paused=False, ai_delay=500):
        self.screen.fill(self.colors["background"])

        tile_size = self.get_dynamic_tile_size(game_state)

        selectable_tiles = game_state.get_selectable_tiles()
        valid_target_tiles = game_state.get_valid_target_tiles()

        for row in game_state.grid.tiles:
            for tile in row:
                self.draw_tile(
                    tile,
                    game_state,
                    tile_size,
                    game_state.selected_tile,
                    selectable_tiles,
                    valid_target_tiles,
                )

        self.draw_player_legend(game_state, tile_size, paused, ai_delay)
        self.draw_event_log(game_state, tile_size)

    def draw_tile(
        self,
        tile,
        game_state,
        tile_size,
        selected_tile=None,
        selectable_tiles=None,
        valid_target_tiles=None,
    ):
        selectable_tiles = selectable_tiles or []
        valid_target_tiles = valid_target_tiles or []

        x = tile.x * tile_size
        y = tile.y * tile_size
        rect = pygame.Rect(x, y, tile_size, tile_size)

        if tile.owner is None:
            color = self.colors["neutral"]
        else:
            color = game_state.players[tile.owner]["color"]

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.colors["grid"], rect, 2)

        if tile in selectable_tiles:
            inset_rect = rect.inflate(-8, -8)
            pygame.draw.rect(self.screen, self.colors["selectable"], inset_rect, 3)

        if tile in valid_target_tiles:
            if tile.owner is not None and tile.owner != game_state.current_player:
                outline_color = self.colors["enemy_target"]
            else:
                outline_color = self.colors["target"]

            pygame.draw.rect(self.screen, outline_color, rect, 4)

        if selected_tile and tile.x == selected_tile.x and tile.y == selected_tile.y:
            pygame.draw.rect(self.screen, self.colors["selected"], rect, 6)

    def draw_player_legend(self, game_state, tile_size, paused=False, ai_delay=500):
        start_x = self.get_sidebar_x(game_state, tile_size)
        start_y = 20

        width, height = self.screen.get_size()
        panel_rect = pygame.Rect(start_x - 15, 0, width - start_x + 15, height)
        pygame.draw.rect(self.screen, self.colors["panel"], panel_rect)

        status = "PAUSED" if paused else "RUNNING"
        speed_text = f"AI Delay: {ai_delay}ms"

        top_lines = [
            f"Turn: {game_state.turn_count}",
            f"Status: {status}",
            speed_text,
            "",
            "Controls:",
            "+/- = AI speed",
            "P = pause",
            "N = step turn",
            "R = restart",
            "H = setup",
            "",
            "Players:",
        ]

        y = start_y
        for line in top_lines:
            text = self.small_font.render(line, True, self.colors["text"])
            self.screen.blit(text, (start_x, y))
            y += 22

        for player_id, profile in game_state.players.items():
            y += 6
            color_box = pygame.Rect(start_x, y + 4, 16, 16)

            if player_id in game_state.eliminated_players:
                pygame.draw.rect(self.screen, self.colors["eliminated"], color_box)
                label_color = self.colors["eliminated"]
            else:
                pygame.draw.rect(self.screen, profile["color"], color_box)
                label_color = self.colors["text"]

            label = f"{profile['name']} ({profile['type'].upper()})"

            if player_id in game_state.eliminated_players:
                label += " - OUT"
            elif player_id == game_state.current_player:
                label += " <- Turn"

            text = self.small_font.render(label[:42], True, label_color)
            self.screen.blit(text, (start_x + 25, y))
            y += 24

    def draw_event_log(self, game_state, tile_size):
        start_x = self.get_sidebar_x(game_state, tile_size)
        _, height = self.screen.get_size()

        start_y = max(430, height - 170)

        title = self.small_font.render("Event Log:", True, self.colors["text"])
        self.screen.blit(title, (start_x, start_y))

        y = start_y + 24
        for event in game_state.event_log:
            text = self.small_font.render(event[:38], True, self.colors["accent"])
            self.screen.blit(text, (start_x, y))
            y += 22

    def draw_game_over_overlay(self, game_state):
        width, height = self.screen.get_size()
        winner_profile = game_state.players[game_state.winner]

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("Game Over", True, self.colors["text"])
        self.screen.blit(title, title.get_rect(center=(width // 2, height // 2 - 70)))

        winner_text = f"Winner: {winner_profile['name']}"
        winner_surface = self.subtitle_font.render(
            winner_text,
            True,
            winner_profile["color"],
        )
        self.screen.blit(
            winner_surface,
            winner_surface.get_rect(center=(width // 2, height // 2 - 10)),
        )

        prompt = self.font.render(
            "R = restart match   |   H = return to setup   |   close window to quit",
            True,
            self.colors["accent"],
        )
        self.screen.blit(
            prompt,
            prompt.get_rect(center=(width // 2, height // 2 + 45)),
        )