def resolve_combat(attacker_tile, defender_tile):
    if attacker_tile.units <= 1:
        return False

    attacking_units = attacker_tile.units - 1

    if attacking_units > defender_tile.units:
        defender_tile.owner = attacker_tile.owner
        defender_tile.units = attacking_units - defender_tile.units
        attacker_tile.units = 1
        return True
    else:
        attacker_tile.units = 1
        defender_tile.units -= attacking_units
        if defender_tile.units < 1:
            defender_tile.units = 1
        return False