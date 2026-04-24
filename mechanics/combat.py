import random


def resolve_capture(attacker_tile, target_tile, capture_chance=0.65):
    if target_tile.owner is None:
        target_tile.owner = attacker_tile.owner
        return True

    if target_tile.owner == attacker_tile.owner:
        return False

    if random.random() <= capture_chance:
        target_tile.owner = attacker_tile.owner
        return True

    return False