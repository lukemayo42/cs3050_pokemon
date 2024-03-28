from move import move
from pokemon import pokemon
import pandas as pd


#function to read stats from pkm_csv and create pokemon object

df = pd.read_csv('pkm_csv.csv')

#reads pokemon data from file based on name given as argument
#returns pokemon object based on data in file and moves given as argument
def create_pokemon(name, df, moves):
    type1 = df.at[df.index[df["Name"] == name].to_list()[0], "Type 1"]
    type2 = df.at[df.index[df["Name"] == name].to_list()[0], "Type 2"]
    hp = int(df.at[df.index[df["Name"] == name].to_list()[0], "HP"])
    attack = int(df.at[df.index[df["Name"] == name].to_list()[0], "Attack"])
    defense = int(df.at[df.index[df["Name"] == name].to_list()[0], "Defense"])
    speed = int(df.at[df.index[df["Name"] == name].to_list()[0], "Speed"])
    return pokemon(name, [type1, type2], moves, hp, attack, defense, speed)
    
    
# Create all pokemon that will be in the game


#create bulbasuar
tackle = move("Tackle", "Normal", 40, 100, "Normal", True)
vine_whip = move("Vine Whip", "Vine Whip", 40, 100, "Grass", True)
venoshock = move("Venoshock", "Venoshock", 65, 100, "Poison", True)
power_whip = move("Power Whip", "Power Whip", 120, 85, "Grass", True)
moves = [tackle, vine_whip, venoshock, power_whip]
bulbasaur = create_pokemon("Bulbasaur", df, moves)

#create charizard
flamethrower = move("Flamethrower", "Fire", 90, 100, "Fire", True)
dragon_claw = move("Dragon Claw", "Dragon Claw", 80, 100, "Dragon", True)
air_slash = move("Air Slash", "Flying", 75, 95, "Flying", True)
inferno = move("Inferno", "Fire", 100, 50, "Fire", True)
charizard = create_pokemon("Charizard", df, [flamethrower, dragon_claw, air_slash, inferno])
enemy_charizard = pokemon(charizard)

#create pikachu
thunderbolt = move("Thunderbolt", "electric", 90, 100, "Electric", True)
quick_attack = move("Quick Attack", "This move always goes first", 40, 100, "Electric", True)
thunder = move("Thunder", "electric", 110, 70, "Electric", True)
iron_tail = move("Iron Tail", "steel", 100, 75, "Steel", True)
pikachu = create_pokemon("Pikachu", df, [thunderbolt, quick_attack, thunder, iron_tail])


#create Pidgeotto
steel_wing = move("Steel Wing", "steel", 70, 90, "Steel", True)
aerial_ace = move("Aerial_Ace", "This move never misses", 60, 100, "Flying", True)
hurricane = move("Hurricane", "flying", 110, 70, "Flying", True)
pidgeotto = create_pokemon("Pidgeotto", df, [steel_wing, aerial_ace, quick_attack, hurricane])


#create gengar
dark_pulse = move("Dark Pulse", "dark", 80, 100, "Dark", True)
shadow_ball = move("Shadow Ball", "ghost", 80, 100, "Ghost", True)
gengar = create_pokemon("Gengar", df, [dark_pulse, shadow_ball, venoshock, thunderbolt])


#create butterfree
#bug_buzz = move("")




'''
# Create Bulbasaur
type = ["grass", "poison"]
bulbasaur_moves = [move("Tackle", "Normal", 40, 100, "Normal", True), move("Vine Whip", "Vine Whip", 40, 100, "Grass", True),
                       move("Venoshock", "Venoshock", 65, 100, "Poison", True), move("Power Whip", "Power Whip", 120, 85, "grass", True)]
#bulbasaur = pokemon("Bulbasaur", type, bulbasaur_moves, 45, 49, 49, 45)

# Create Ivysaur
type2 = ["Grass", "Poison"]
#ivysaur = pokemon("Ivysaur", type, moves, 60, 62, 63, 60)

# Create Venusaur
type3 = ["Grass", "Poison"]
#venusaur = pokemon("Venusaur", type, moves, 80, 82, 83, 80)

# Create Charmander
type4 = ["Fire"]
#charmander = pokemon("Charmander", type4, moves, 39, 52, 43, 65)

# Create Charmeleon
type5 = ["Fire"]
#charmeleon = pokemon("Charmeleon", type5, moves, 58, 64, 58, 80)

# Create Charizard
type6 = ["fire", "flying"]
charizard_moves = [move("Flamethrower", "fire", 90, 100, "fire", True), move("Dragon Claw", "Dragon Claw", 80, 100, "dragon", True),
                       move("Air Slash", "flying", 75, 95, "flying", True), move("Inferno", "fire", 100, 50, "fire", True)]
charizard = pokemon("Charizard", type6, charizard_moves, 78, 84, 78, 100)
'''