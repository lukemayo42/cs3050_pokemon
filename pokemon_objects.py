from move import move
from pokemon import pokemon

# Create all pokemon that will be in the game

moves = []

# Create Bulbasaur
type = ["Grass", "Poison"]
bulbasaur_moves = [move("Tackle", "Normal", 40, 100, "Normal", True), move("Vine Whip", "Vine Whip", 40, 100, "Grass", True),
                       move("Venoshock", "Venoshock", 65, 100, "Poison", True), move("Power Whip", "Power Whip", 120, 85, "Grass", True)]
bulbasaur = pokemon("Bulbasaur", type, bulbasaur_moves, 45, 49, 49, 45)

# Create Ivysaur
type2 = ["Grass", "Poison"]
ivysaur = pokemon("Ivysaur", type, moves, 60, 62, 63, 60)

# Create Venusaur
type3 = ["Grass", "Poison"]
venusaur = pokemon("Venusaur", type, moves, 80, 82, 83, 80)

# Create Charmander
type4 = ["Fire"]
charmander = pokemon("Charmander", type4, moves, 39, 52, 43, 65)

# Create Charmeleon
type5 = ["Fire"]
charmeleon = pokemon("Charmeleon", type5, moves, 58, 64, 58, 80)

# Create Charizard
type6 = ["Fire", "Flying"]
charizard_moves = [move("Flamethrower", "Fire", 90, 100, "Fire", True), move("Dragon Claw", "Dragon Claw", 80, 100, "Dragon", True),
                       move("Air Slash", "Flying", 75, 95, "Flying", True), move("Inferno", "Fire", 100, 50, "Fire", True)]
charizard = pokemon("Charizard", type6, charizard_moves, 78, 84, 78, 100)
