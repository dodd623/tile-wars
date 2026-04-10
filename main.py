import pygame
from engine.game_state import GameState
from ui.renderer import Renderer


def main():
    pygame.init()

    game_state = GameState()

    tile_size = 60
    width = game_state.grid.width * tile_size
    height = game_state.grid.height * tile_size

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Silent Front")

    renderer = Renderer(screen, tile_size)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state.game_phase == "start":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state.start_game()

            elif game_state.game_phase == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and game_state.is_player_turn():
                    x, y = pygame.mouse.get_pos()

                    grid_x = x // tile_size
                    grid_y = y // tile_size

                    tile = game_state.grid.get_tile(grid_x, grid_y)
                    game_state.handle_player_click(tile)

        renderer.draw(game_state)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()