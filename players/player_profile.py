DEFAULT_PLAYER_COLORS = [
    {"name": "Blue", "value": (70, 130, 180)},
    {"name": "Red", "value": (180, 70, 70)},
    {"name": "Green", "value": (80, 160, 90)},
    {"name": "Gold", "value": (180, 150, 70)},
    {"name": "Purple", "value": (140, 90, 180)},
    {"name": "Teal", "value": (70, 160, 160)},
    {"name": "Orange", "value": (200, 110, 60)},
    {"name": "Pink", "value": (160, 80, 130)},
]


def create_player_profiles(num_players=2, human_players=1):
    players = {}

    for player_id in range(num_players):
        player_type = "human" if player_id < human_players else "ai"
        default_name = (
            f"Player {player_id + 1}"
            if player_type == "human"
            else f"AI {player_id + 1}"
        )

        color_data = DEFAULT_PLAYER_COLORS[player_id]

        players[player_id] = {
            "id": player_id,
            "name": default_name,
            "type": player_type,
            "color": color_data["value"],
            "color_name": color_data["name"],
            "color_index": player_id,
        }

    return players