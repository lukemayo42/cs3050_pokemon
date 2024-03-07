from pokemon import pokemon
from move import move
from Character import Character
import random
import pokemon_objects

#make item class later
#we are assuming that we are receiving the type of button that is pressed (pokemon, move, item) and the specific move/pokemon/item that is used/switched
#please write a method in the button class which we can call that will give us a list containing the type of button that 

# def battle(player, enemy, btn_info):
#     #while loop to check if both players have pokemon left
#     if (player.chk_party() and enemy.chk_party()):
#         player_pkm = player.get_curr_pkm()
#         enemy_pkm = enemy.get_curr_pkm()
#     #loop to check if pokemon are fainted, throw out first pokemon
#         #spd_flag = chk_spd(player_pkm, enemy_pkm)
#         if chk_spd(player_pkm, enemy_pkm):
#             player_action = player_turn(player, enemy, btn_info)
#             if not enemy.chk_party():
#                 # tell gui player wins
#                 break
#             elif enemy.get_curr_pkm().get_is_fainted():
#                 # force enemy to switch pokemon
#                 pass
#             else:
#                 enemy_action = enemy_turn(enemy, player)
#                 # send to gui
#         else:
#             enemy_action = enemy_turn(enemy, player)
#             if not player.chk_party():
#                 # tell gui enemy wins
#                 break
#             elif player.get_curr_pkm().get_is_fainted():
#                 # force player to switch pokemon
#                 pass
#             else:
#                 # btn_info = get_btn_info()
#                 player_action = player_turn(enemy, player)
#                 # send to gui

# Battle function without while loop
def battle(player, enemy, btn_info):
    player_pkm = player.get_curr_pkm()
    enemy_pkm = enemy.get_curr_pkm()
    
    #if player pokemon faster than enemy pokemon
    if chk_spd(player_pkm, enemy_pkm):
        player_action = player_turn(player, enemy, btn_info)
        # If the player took a fight action and the move hit:
        if player_action:
            # Update Gui
            pass
        else:
            # Update Gui
            pass
        if not enemy.chk_party():
            # tell gui player wins
            pass
        elif enemy.get_curr_pkm().get_is_fainted():
            # force enemy to switch pokemon
            pass
        else:
            enemy_action = enemy_turn(enemy, player)
            if enemy_action:
                # Update Gui
                print("the move hit")
            else:
                # Update Gui
                print("The move didn't hit")
            if not player.chk_party():
                # tell gui enemy wins
                pass
            elif player.get_curr_pkm().get_is_fainted():
                # force player to switch pokemon
                pass
            # send to gui
    else:
        enemy_action = enemy_turn(enemy, player)
        if enemy_action:
            # Update Gui
            pass
        else:
            # Update Gui
            pass
        if not player.chk_party():
            # tell gui enemy wins
            pass
        elif player.get_curr_pkm().get_is_fainted():
            # force player to switch pokemon
            pass
        else:
            player_action = player_turn(player, enemy, btn_info)
            if player_action:
                # Update Gui
                pass
            else:
                # Update Gui
                pass
            if not enemy.chk_party():
                # tell gui player wins
                pass
            elif enemy.get_curr_pkm().get_is_fainted():
                # force enemy to switch pokemon
                pass
            # send to gui


    #check speed to see which pokemon goes first
    #get back choice from gui/controller
    #take player or enemy turns based on speed
    #check is a pokemon is fainted switch out if pokemon left - if not end battle
    

    

#player is a character object
#button info is a alist containing the type of button and the move/item/pokemon switched - gives index of nrew pokemon to be put into 0 index in list
#returns bool whether action was succesful
def player_turn(player, enemy, btn_info):
    action = True
    #if move, it item, if swtich pokemon
    if btn_info[0] == "move":
        move_used = btn_info[1]
        if roll_accuracy(move_used):
            #send gui sometyhing saying it hit 
            dmg = calc_dmg(player.get_curr_pkm(), enemy.get_curr_pkm(), move_used)
            enemy.get_curr_pkm().remove_health(dmg)
            print(player.get_curr_pkm().move_to_string(move_used, True))
        else:
            #send gui something saying it missed
            print(player.get_curr_pkm().move_to_string(move_used, False))
            action = False
        
    #item
    elif btn_info[0] == "item":
        pass
    #switch
    else:
        #call switch pokemon function
        pass

    #if move calc damage using index 0 of both player and enemy
    #update curr health of enemy
    return action

#single turn of an enemy character, takes in character and player 
def enemy_turn(enemy, player):
    action_str = "move"
    action_flag = True
    #randomly choose move
    move_index = random.randint(0,3)
    move_used = enemy.get_curr_pkm().get_moves()[move_index]
    if action_str == "move":
        if roll_accuracy(move_used):
            #send gui sometyhing sayinssg it hit 
            dmg = calc_dmg(enemy.get_curr_pkm(), player.get_curr_pkm(), move_used)
            player.get_curr_pkm().remove_health(dmg)
            print(enemy.get_curr_pkm().move_to_string(move_used, True))
        else:
            #send gui something saying it missed
            print(enemy.get_curr_pkm().move_to_string(move_used, False))
            action_flag = False
        
    #item
    elif action_str == "item":
        pass
    #switch
    else:
        #call switch pokemon function
        pass
    #maybe later add intelligence
    
    #calc damg
    #update curr health of player
    return action_flag

def switch():
    pass


#calcualtes damage for a move, given atk for the pokemon using the move, def of the pokemon getting hit, and the move being used
def calc_dmg(atk_pkm, def_pkm, move):
    level = 50
    #may want to add STAB - same type attack bonus - 1.5 if move type  matches pokemon type
    #write chk_effective later
    #STAB * TYPE 1 EFFECTIVE * TYPE 2 EFFECTIVE at end of equation
    #random variable in damage equation
    random_variable = random.randint(217, 255) / 255
    dmg = (((((2 * level * roll_crit())/5) + 2)* move.get_power() * (atk_pkm.get_curr_atk()/def_pkm.get_curr_def())/50) + 2 ) * random_variable
    return dmg

#rerturns 1 if user spedd is greater then enemy otherwise 0
def chk_spd(user_pkm, enemy_pkm):
    if(user_pkm.get_curr_spd() > enemy_pkm.get_curr_spd()):
        return True
    else:
        return False
    pass

def use_item():
    pass

#returns 1 or 2 to roll crit
def roll_crit():
    rand_list = [1, 1, 1, 1, 1, 1, 1, 1, 2]
    return random.choice(rand_list)


def chk_effective():
    pass

#returns 1 if move hits, 0 if move misses
def roll_accuracy(move):
    if move.get_accuracy() == 100:
        return True
    elif (random.randint(0, 100)) <= move.get_accuracy():
        return True
    else:
        return False



def main():
    pokemon_bag = [pokemon_objects.bulbasaur, pokemon_objects.charazard]

    trainer1 = Character("Ash", pokemon_bag, [], 1000,
                              "I'm on a journey to become a Pokemon Master!")

    trainer2 = Character("Misty", pokemon_bag, [], 800, "Water types are the best!")