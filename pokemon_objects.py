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
    hp*=1.3
    hp = int(hp)
    attack = int(df.at[df.index[df["Name"] == name].to_list()[0], "Attack"])
    defense = int(df.at[df.index[df["Name"] == name].to_list()[0], "Defense"])
    speed = int(df.at[df.index[df["Name"] == name].to_list()[0], "Speed"])
    #check to see if type2 is a string(meaning it has a value) if not do not include type2 in declaration of pokemon object
    if not isinstance(type2, str):
        return pokemon(name, [type1], moves, hp, attack, defense, speed)
    return pokemon(name, [type1, type2], moves, hp, attack, defense, speed)
    
    
# Create all pokemon that will be in the game


#create bulbasuar
tackle = move("Tackle", "Normal", 40, 100, "Normal", True)
vine_whip = move("Vine Whip", "Vine Whip", 40, 100, "Grass", True)
venoshock = move("Venoshock", "Venoshock", 65, 100, "Poison", True)
power_whip = move("Power Whip", "Power Whip", 120, 85, "Grass", True)
moves = [tackle, vine_whip, venoshock, power_whip]
bulbasaur = create_pokemon("Bulbasaur", df, moves)
enemy_bulbasaur = pokemon(bulbasaur)

#create charizard
flamethrower = move("Flamethrower", "Fire", 90, 100, "Fire", True)
dragon_claw = move("Dragon Claw", "Dragon Claw", 80, 100, "Dragon", True)
air_slash = move("Air Slash", "Flying", 75, 95, "Flying", True)
inferno = move("Inferno", "Fire", 100, 50, "Fire", True)
charizard = create_pokemon("Charizard", df, [flamethrower, dragon_claw, air_slash, inferno])
enemy_charizard = pokemon(charizard)

#create pikachu
thunderbolt = move("Thunderbolt", "electric", 90, 100, "Electric", True)
quick_attack = move("Quick Attack", "priority", 40, 100, "Electric", True)
thunder = move("Thunder", "electric", 110, 70, "Electric", True)
iron_tail = move("Iron Tail", "steel", 100, 75, "Steel", True)
pikachu = create_pokemon("Pikachu", df, [thunderbolt, quick_attack, thunder, iron_tail])
enemy_pikachu = pokemon(pikachu)

#create Pidgeotto
steel_wing = move("Steel Wing", "steel", 70, 90, "Steel", True)
aerial_ace = move("Aerial_Ace", "This move never misses", 60, 100, "Flying", True)
hurricane = move("Hurricane", "flying", 110, 70, "Flying", True)
pidgeotto = create_pokemon("Pidgeotto", df, [steel_wing, aerial_ace, quick_attack, hurricane])
enemy_pidgeotto = pokemon(pidgeotto)

#create gengar
dark_pulse = move("Dark Pulse", "dark", 80, 100, "Dark", True)
shadow_ball = move("Shadow Ball", "ghost", 80, 100, "Ghost", True)
gengar = create_pokemon("Gengar", df, [dark_pulse, shadow_ball, venoshock, thunderbolt])
enemy_gengar = pokemon(gengar)

#create butterfree
bug_buzz = move("Bug Buzz", "bug", 90, 100, "Bug", True)
psybeam = move("Psybeam", "psychic", 65, 100, "Psychic", True)
butterfree = create_pokemon("Butterfree", df, [bug_buzz, psybeam, aerial_ace, venoshock])
enemy_butterfree = pokemon(butterfree)


#create slowbro
surf = move("Surf", "water", 90, 100, "Water", True)
headbutt = move("Headbutt", "normal", 70, 100, "Normal", True)
bulldoze = move("Bulldoze", "ground", 60, 100, "Ground", True)
psychic = move("Psychic", 'pshychic', 90, 100, "Psychic", True)
slowbro = create_pokemon("Slowbro", df, [surf, psychic, headbutt, bulldoze])
enemy_slowbro = pokemon(slowbro)

#create lucario
aura_sphere = move("Aura Sphere", "fighting", 80, 100, "Fighting", True)
cross_chop = move("Cross Chop", "fighting", 100, 80, "Fighting", True)
metal_claw = move("Metal Claw", "fighting", 50, 95, "Steel", True)
lucario = create_pokemon("Lucario", df, [aura_sphere, cross_chop, metal_claw, aerial_ace])
enemy_lucario = pokemon(lucario)

#create crobat
x_scissor = move("X-Scissor", "bug", 80, 100, "Bug", True)
crobat = create_pokemon("Crobat", df, [air_slash, venoshock, steel_wing, x_scissor])
enemy_crobat = pokemon(crobat)

#create shiftry
leaf_blade = move("Leaf Blade", "grass", 90, 100, "Grass", True)
foul_play = move("Foul Play", "dark", 95, 100, "Dark", True)
shiftry = create_pokemon("Shiftry", df, [leaf_blade, air_slash, foul_play, x_scissor])
enemy_shiftry = pokemon(shiftry)

#create scyther
wing_attack = move("Wing Attack", "flying", 60, 100, "Flying", True)
slash = move("Slash", "normal", 70, 100, "Flying", True)
scyther = create_pokemon("Scyther", df, [wing_attack, slash, air_slash, x_scissor])
enemy_scyther = pokemon(scyther)

#create mr.mime
mr_mime = create_pokemon("Mr.Mime", df, [psychic, thunder, aerial_ace, psybeam])
enemy_mr_mime = pokemon(mr_mime)


#create wooper
ice_beam = move("Ice Beam", "ice", 90, 100, "Ice", True)
earthquake = move("Earthquake", "ground", 100, 100, "Ground", True)
sludge_bomb = move("Sludge Bomb", "posion", 90, 100, True)
wooper = create_pokemon("Wooper", df, [surf, ice_beam, earthquake, sludge_bomb])

#create noctowl
extrasensory = move("Extrasensory", "psychic", 80, 100, "Psychic", True)
swift = move("Swift", "normal", 60, 100, "Normal", True)
noctowl = create_pokemon("Noctowl", df, [air_slash, swift, extrasensory, shadow_ball])
enemy_noctowl = pokemon(noctowl)

#create Dragonite


#create heracross


#create piloswine


#create farfetchd


#create gliscor



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