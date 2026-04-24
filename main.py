import pygame
from engine.game_state import GameState
from players.ai_basic import BasicAI
from ui.renderer import Renderer


def build_ai_players(game_state):
    return {
        player_id: BasicAI(player_id=player_id)
        for player_id, profile in game_state.players.items()
        if profile["type"] == "ai"
    }


def main():
    pygame.init()

    game_state = GameState()

    tile_size = 40
    width = 1200
    height = 850

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Tile Wars")

    renderer = Renderer(screen, tile_size)

    clock = pygame.time.Clock()
    running = True

    ai_players = {}
    ai_move_delay = 500
    ai_turn_start_time = None

    paused = False
    step_once = False

    editing_name = False
    name_input = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state.game_phase == "setup":
                if event.type == pygame.KEYDOWN:
                    if editing_name:
                        if event.key == pygame.K_RETURN:
                            game_state.rename_selected_player(name_input)
                            editing_name = False
                            name_input = ""
                        elif event.key == pygame.K_ESCAPE:
                            editing_name = False
                            name_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            name_input = name_input[:-1]
                        elif len(name_input) < 16 and event.unicode.isprintable():
                            name_input += event.unicode

                    else:
                        if event.key == pygame.K_UP:
                            game_state.increase_total_players()
                        elif event.key == pygame.K_DOWN:
                            game_state.decrease_total_players()
                        elif event.key == pygame.K_RIGHT:
                            game_state.increase_human_players()
                        elif event.key == pygame.K_LEFT:
                            game_state.decrease_human_players()
                        elif event.key == pygame.K_g:
                            game_state.cycle_grid_size()
                        elif event.key == pygame.K_TAB:
                            game_state.next_setup_player()
                        elif event.key == pygame.K_c:
                            game_state.cycle_selected_player_color()
                        elif event.key == pygame.K_n:
                            editing_name = True
                            selected_profile = game_state.players[
                                game_state.selected_setup_player
                            ]
                            name_input = selected_profile["name"]
                        elif event.key == pygame.K_SPACE:
                            game_state.start_game()
                            ai_players = build_ai_players(game_state)
                            paused = False
                            step_once = False

            elif game_state.game_phase in ["playing", "game_over"]:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS]:
                        ai_move_delay = max(50, ai_move_delay - 100)

                    elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                        ai_move_delay = min(2000, ai_move_delay + 100)

                    elif event.key == pygame.K_p:
                        paused = not paused

                    elif event.key == pygame.K_n:
                        step_once = True

                    elif event.key == pygame.K_r:
                        game_state.restart_game()
                        ai_players = build_ai_players(game_state)
                        paused = False
                        step_once = False

                    elif event.key == pygame.K_h:
                        game_state.return_to_setup()
                        ai_players = {}
                        paused = False
                        step_once = False

                if (
                    game_state.game_phase == "playing"
                    and event.type == pygame.MOUSEBUTTONDOWN
                    and game_state.is_human_turn()
                    and not paused
                ):
                    x, y = pygame.mouse.get_pos()

                    grid_x = x // tile_size
                    grid_y = y // tile_size

                    tile = game_state.grid.get_tile(grid_x, grid_y)
                    game_state.handle_player_click(tile)

        ai_can_move = (
            game_state.game_phase == "playing"
            and game_state.is_ai_turn()
            and (not paused or step_once)
        )

        if ai_can_move:
            if ai_turn_start_time is None:
                ai_turn_start_time = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()

            if step_once or current_time - ai_turn_start_time >= ai_move_delay:
                current_ai = ai_players[game_state.get_current_player()]
                current_ai.take_turn(game_state)
                ai_turn_start_time = None
                step_once = False
        else:
            ai_turn_start_time = None

        renderer.draw(
            game_state,
            editing_name=editing_name,
            name_input=name_input,
            paused=paused,
            ai_delay=ai_move_delay,
        )

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()