from item import item

# Create all the items that will be in the game
potion = item("Potion", "A spray-type medicine for treating wounds. It can be used to restore 20 HP to a Pokémon.",
              200, 20, False)

super_potion = item("Super Potion", "A spray-type medicine for treating wounds. It can be used to restore 60 HP to a Pokémon.",
                    700, 60, False)

hyper_potion = item("Hyper Potion", "A spray-type medicine for treating wounds. "
                                    "It can be used to restore 120 HP to a Pokémon.", 1500, 120, False)

max_potion = item("Max Potion", "A spray-type medicine for treating wounds. It can be used to fully restore the max HP of a Pokémon.",
                  2500, 10000, False)

# revive = item("Revive", "A medicine that can be used to revive a Pokémon that has fainted. It also restores half the Pokémon's max HP",
#               2000, 10, True)
