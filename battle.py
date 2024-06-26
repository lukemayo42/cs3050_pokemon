from pokemon import pokemon
from move import move
from Character import Character
import random
import pokemon_objects
import time

#we are assuming that we are receiving the type of button that is pressed (pokemon, move, item) and the specific move/pokemon/item that is used/switched
#please write a method in the button class which we can call that will give us a list containing the type of button that 

#some things that i have noticed/ am concerned about: when you swap in the gui, the pokemon automatically swaps, this is not how the game works, the pokemon
#that is swapped based on the current pokemon's speed, if the other pokemon has a faster speed, that pokemon attack the current pokemon first, 
#then the players pokemon is swapped after, the same is true for items, if an item is used and the opponents pokemon is faster that pokemon goes first
#then the item is used
#2. if the text bubble is updated in battle, will it be rendered in the gui?, or will it have to wait for battle to be returned for the gui to be updated
# in this case, it may be better to do the logic, waiting, and updated text bubble in the gui
#ideas for text bubble waiting in battle - wait using threads in the backend
# the battle logic/ implementation may need to change

#idea for waiting and text bubbles - invisible timer - set timer to 0 and set condition to continue after x amount of time - using deltatime
#timer = 0 //using deltatime
# if timer > 5:
#   continue;

#wierd thing happening with charizard and bulbasuar swapping: heres what I think is happening
#user is faster than enemy so bulbasuar gets thrown out, bulbasuar is out and battle is called, 
#bulbasaur faints and for some reason gui then automatically renders charizard back out as pokemon

#when you swap and the current pokemon faints sometimes the message doesnt get printed in the terminal

#returns 2 strings, what move player did and what move the enemy did
#TODO:implement the text bubble from gui and add as parameter
def battle(player, enemy, btn_info):
    #TODO: fix battle logic 
    player_pkm = player.get_curr_pkm()
    enemy_pkm = enemy.get_curr_pkm()
    force_swap = False
    action_list = []
    #if player pokemon faster than enemy pokemon
    if chk_spd(player_pkm, enemy_pkm):
        player_action = player_turn(player, enemy, btn_info)
        action_list.append(["player", btn_info[0], player_action]) 
        # If enemy's party is out of pokemon
        if not enemy.chk_party():
            #TODO: update text bubble to "The enemy is out of pokemon! You Win!"
            # For now we need to do this to make sure we don't reference something without assignment
            player_action = "win"
            enemy_action = "lose"
            
        #force enemy to switch pokemon if current pokemon is fainted - takes up enemy's turn
        elif enemy.get_curr_pkm().get_is_fainted():
            force_swap = True
            action_list.append(["enemy", "fainted", f"{enemy.get_curr_pkm().get_name()} fainted"])
            print(f"{enemy.get_curr_pkm().get_name()} fainted")
            enemy_action, action_str = enemy_turn(enemy, player, force_swap)
            action_list.append(["enemy", action_str, enemy_action])
            
        #enemy pokemon has not fainted
        else:
            enemy_action, action_str = enemy_turn(enemy, player, force_swap)
            action_list.append(["enemy", action_str, enemy_action])
            if not player.chk_party():
                #TODO: update check bubble to say player lost
                # For now we need to do this to make sure we don't reference something without assignment
                player_action = "lose"
                enemy_action = "win"
            elif player.get_curr_pkm().get_is_fainted():
                # force player to switch pokemon
                #TODO: updat text bubble saying that that the current pokemon ais died and prompt user to switch
                # For now we need to do this to make sure we don't reference something without assignment
                player_action = "fainted"
                print(f"{player.get_curr_pkm().get_name()} fainted")
                action_list.append(["player", "fainted", f"{player.get_curr_pkm().get_name()} fainted"])
                #TODO: get string and action string from swap pokemon and add it to action_dict
                #force player to switch
            # send to gui
    # if enemy pokemon faster than player pokemon
    else:
        # Take enemy action
        enemy_action, action_str = enemy_turn(enemy, player, force_swap)
        action_list.append(["enemy", action_str, enemy_action])
        # If the player party is fully fainted
        if not player.chk_party():
            # TODO: update text bubble saying that the player has lost
            # For now we need to do this to make sure we don't reference something without assignment
            player_action = "lose"
            enemy_action = "win"
        # If the current pokemon in the players party is fainted, make them switch pokemon
        elif player.get_curr_pkm().get_is_fainted():
            # force player to switch pokemon
            force_swap = True
            #update player_turn to handle force switch case
            player_action = "fainted"
            print(f"{player.get_curr_pkm().get_name()} fainted")
            action_list.append(["player", "fainted", f"{player.get_curr_pkm().get_name()} fainted"])
            
            #TODO: fix this case - player pokemon is faster than enemy pokemon, and the player pokemon faints, current pokemon stays the same without prompt being asked
        # The enemy turn didn't result in anything needing the player to do anything
        else:
            player_action = player_turn(player, enemy, btn_info)
            # If the player turn results in the enemy's party being all fainted
            action_list.append(["player", btn_info[0], player_action])

            if not enemy.chk_party():
                # tell gui player wins
                player_action = "win"
                enemy_action  = "lose"
            # If the enemy's current pokemon is fainted, make them switch
            elif enemy.get_curr_pkm().get_is_fainted():
                # force enemy to switch pokemon
                force_swap = True
                action_list.append(["enemy", "fainted", f"{enemy.get_curr_pkm().get_name()} fainted"])
                print(f"{enemy.get_curr_pkm().get_name()} fainted")
                enemy_action, action_str = enemy_turn(enemy, player, force_swap)
                action_list.append(["enemy", "swap", enemy_action])

            # send to gui
    # Return the first action that was done and the second action that was done
    return player_action, enemy_action, action_list
    
#this function reads an action string and determines what the action was and adds it to the given dictionary
def add_to_dict(action):
    pass
#player is a character object
#button info is a alist containing the type of button and the move/item/pokemon switched - gives index of nrew pokemon to be put into 0 index in list
#returns bool whether action was succesful
def player_turn(player, enemy, btn_info):
    #if move, it item, if switch pokemon
    if btn_info[0] == "move":
        move_used = btn_info[1]
        if roll_accuracy(move_used):
            #send gui sometyhing saying it hit 
            dmg, effectiveness, crit = calc_dmg(player.get_curr_pkm(), enemy.get_curr_pkm(), move_used)
            enemy.get_curr_pkm().remove_health(dmg)
            
            #print(f"enemy health: {enemy.get_current_pokemon().get_curr_hlth()}")
            enemy.get_curr_pkm().set_hlth_after_move(enemy.get_curr_pkm().get_curr_hlth())
            action_str = player.get_curr_pkm().move_to_string(move_used, True, effectiveness, crit, player)
            print(action_str)
        else:
            #send gui something saying it missed
            #print(f"enemy health: {enemy.get_current_pokemon().get_curr_hlth()}")
            enemy.get_curr_pkm().set_hlth_after_move(enemy.get_curr_pkm().get_curr_hlth())
            action_str = player.get_curr_pkm().move_to_string(move_used, False, 10, 1, player)
            print(action_str)
        
        
    #item
    elif btn_info[0] == "item":
        action_str = "placeholder"
        # Assume that the button info's index 1 will contain the key of the item that is being used.
        for item in player.get_item_bag():
            if btn_info[1] == item:
                item.use_item(player.get_curr_pkm())
                player.get_curr_pkm().set_hlth_after_item(player.get_curr_pkm().get_curr_hlth())
                player.get_item_bag()[item] -= 1
                action_str = item.item_to_string(item, player)
                print(action_str)
    #switch
    else:
        # Call swap pokemon function. The current pokemon is always at index 0, the button info's index 1 will contain
        # the index of the pokemon that is to be swapped in.
        player.swap_pokemon(0, btn_info[1])
        action_str = f"{player.get_name()} swapped out {player.get_pokemon_list()[btn_info[1]].get_name()} with {player.get_curr_pkm().get_name()}"
        print(action_str)

    #if move calc damage using index 0 of both player and enemy
    #update curr health of enemy
    return action_str
'''
def set_prev_pkm(trainer):
    if trainer.get_curr_pkm().get_is_fainted():
        trainer.set_prev_pkm(trainer.get_curr_pkm())
'''
#single turn of an enemy character, takes in enemy, player, and a boolean saying whether the enemy is forced to swap or not
def enemy_turn(enemy, player, force_swap):
    # Need to add this to make sure there is no reference without assignment, although I can't see a case where action is not assigned
    # TODO: Figure out why need this
    action = "placeholder"
    # action is set to placeholder when item is used sometimes
    enemy_pkm = enemy.get_curr_pkm()
    player_pkm = player.get_curr_pkm()
    action_str = "swap"
    if not force_swap:
        action_str = get_enemy_action(enemy)
    '''
    #remove later
    if action_str == "item":
        action_str = "move"
'''
    if action_str == "move":
        # randomly choose move
        move_index = random.randint(0, 3)
        move_used = enemy_pkm.get_moves()[move_index]
        # If the move hits, do damage
        if roll_accuracy(move_used):
            dmg, effectiveness, crit = calc_dmg(enemy_pkm, player_pkm, move_used)
            player_pkm.remove_health(dmg)
            player_pkm.set_hlth_after_move(player_pkm.get_curr_hlth())
            action = enemy_pkm.move_to_string(move_used, True, effectiveness, crit, enemy)
            print(action)
        else:
            player_pkm.set_hlth_after_move(player_pkm.get_curr_hlth())
            action = enemy_pkm.move_to_string(move_used, False, 0, 1, enemy)
            print(action)

    #item
    
    elif action_str == "item":
        action = "placeholder"
        item_is_used = False
        while not item_is_used:
            for item, num_items in enemy.get_item_bag().items():
                use_item = random.choice([True, False])
                # TODO: Impliment enemy being able to use revive item
                # if num_items > 0 and use_item and item.get_name() == "Revive":
                    # pass
                if num_items > 0 and use_item:
                    item.use_item(enemy_pkm)
                    enemy_pkm.set_hlth_after_item(enemy_pkm.get_curr_hlth())
                    enemy.get_item_bag()[item] -= 1
                    action = item.item_to_string(item, enemy)
                    print(action)
                    item_is_used = True
                    break
    #switch
    elif action_str == "swap":
        #call swap pokemon function. Make sure to swap with a pokemon that is not fainted.
        if enemy.get_pokemon_list()[1].get_is_fainted():
            enemy.swap_pokemon(0, 2)
            action = f"{enemy.get_name()} swapped out {enemy.get_pokemon_list()[2].get_name()} with {enemy.get_curr_pkm().get_name()}"
            print(action)
        elif enemy.get_pokemon_list()[2].get_is_fainted():
            enemy.swap_pokemon(0, 1)
            action = f"{enemy.get_name()} swapped out {enemy.get_pokemon_list()[2].get_name()} with {enemy.get_curr_pkm().get_name()}"
            print(action)
        else:
            swap_index = random.randint(1,2)
            enemy.swap_pokemon(0, swap_index)
            action = f"{enemy.get_name()} swapped out {enemy.get_pokemon_list()[swap_index].get_name()} with {enemy.get_curr_pkm().get_name()}"
            print(action)
    #maybe later add intelligence
    
    #calc damg
    #update curr health of player
    return action, action_str


# Function is enemy's "intelligence"
# Function determines the action the enemy will take based upon the amount of health their current pokemon has.
def get_enemy_action(enemy):
    #TODO: Figure out how to do to the probabilities and ranges efficiently
    enemy_pkm = enemy.get_curr_pkm()
    # Randomly pick a number to determine the probability an action is taken.
    probability_range_full = 20
    probability_action = random.randint(0, probability_range_full)
    # If the enemy's current pokemon is at 10% health or less, there is an 85% chance to use an item, a 5% chance to
    # swap pokemon, and a 10% chance to use a move.
    if enemy_pkm.get_curr_hlth() <= (enemy_pkm.get_max_hlth() / 10):
        probability_range_partial = probability_range_full - 1
        action_str = get_action_based_on_probability(probability_action, enemy, probability_range_partial)
    # If the enemy's current pokemon is at 25% health or less, there is an 47.5% chance to use an item, a 5% chance to
    # swap pokemon, and a 47.5% chance to use a move.
    elif enemy_pkm.get_curr_hlth() <= (enemy_pkm.get_max_hlth() / 4):
        probability_range_partial = int(probability_range_full/2) + 1
        action_str = get_action_based_on_probability(probability_action, enemy, probability_range_partial)
    # If the enemy's current pokemon is at 50% health or less, there is an 19% chance to use an item, a 5% chance to
    # swap pokemon, and a 76% chance to use a move.
    elif enemy_pkm.get_curr_hlth() <= (enemy_pkm.get_max_hlth() / 2):
        probability_range_partial = int(probability_range_full/4) + 1
        action_str = get_action_based_on_probability(probability_action, enemy, probability_range_partial)
    else:
        action_str = "move"

    return action_str

# Function is a helper function for get_enemy_action(enemy)
# Function takes in probability_action, enemy, and probability_range. Based on the probability_action and the given
# probability_range, the function will determine the action the enemy will take.
def get_action_based_on_probability(probability_action, enemy, probability_range):
    # probability_action = 0
    has_items = False

    for num_items in enemy.get_item_bag().values():
        if num_items != 0:
            has_items = True

    if probability_action in range(1, probability_range) and has_items:
        action_str = "item"

    elif probability_action == 0:
        # Add this case for testing purposes: TODO: remove when necessary
        if len(enemy.get_pokemon_list()) == 1:
            action_str = "move"
        # Make sure that the enemy player has a pokemon to swap to. If not, change action string to move.
        elif enemy.get_pokemon_list()[1].get_is_fainted() and enemy.get_pokemon_list()[2].get_is_fainted():
            action_str = "move"
        else:
            action_str = "swap"
    else:
        action_str = "move"

    return action_str

#calcualtes damage for a move, given atk for the pokemon using the move, def of the pokemon getting hit, and the move being used
def calc_dmg(atk_pkm, def_pkm, move):
    level = 50
    #may want to add STAB - same type attack bonus - 1.5 if move type  matches pokemon type
    #write chk_effective later
    #STAB * TYPE 1 EFFECTIVE * TYPE 2 EFFECTIVE at end of equation
    #random variable in damage equation
    effectiveness = chk_effective(move, def_pkm)
    crit = roll_crit()

    random_variable = random.randint(217, 255) / 255
    dmg = (((((2 * level * crit)/5) + 2)* move.get_power() * (atk_pkm.get_curr_atk()/def_pkm.get_curr_def())/50) + 2 ) * random_variable * effectiveness
    return dmg , effectiveness, crit

#rerturns True if the user will fo first , false if the enemy will go first
def chk_spd(user_pkm, enemy_pkm):
    user_spd = user_pkm.get_curr_spd()
    enemy_spd = enemy_pkm.get_curr_spd()
    #if user speed is equal to enemy speed flip coin to see who goes first
    if user_spd == enemy_spd:
        rand_list = [True, False]
        return random.choice(rand_list)
    elif(user_pkm.get_curr_spd() > enemy_pkm.get_curr_spd()):
        return True
    else:
        return False


#returns 1 or 2 to roll crit
def roll_crit():
    rand_list = [1, 1, 1, 1, 1, 1, 1, 1, 2]
    return random.choice(rand_list)

#takes in move used and the defending pokemon
#calculates effectivenss vbased on defending pokemon types and move type
#returns effectivenss in number form 1/2 if not very effective 2 or 4 if super effective
#used in damage calculation
def chk_effective(move_used, pkm):
    effectiveness = 1
    move_type = move_used.get_type().lower()
    pkm_types = pkm.get_types()
    pkm_type1 = pkm_types[0].lower()
    pkm_type2 = "none"
    if len(pkm_types) > 1:
        pkm_type2 = pkm_types[1].lower()
    #defense pokemon water
    if pkm_type1 == "water" or pkm_type2 == "water":
        #not very effective moves
        if move_type == "fire" or move_type == "water" or move_type == "ice" or move_type == "steel":
            effectiveness/=2
        #super effective moves
        elif move_type == "electric" or move_type == "grass":
            effectiveness*=2
    #defending pokemon type fire
    if pkm_type1 == "fire" or pkm_type2 == "fire":
        #not very effective move types
        if move_type == "fire" or move_type == "grass" or move_type == "ice" or move_type == "bug" or move_type == "steel":
            effectiveness/=2
        #super effective moves
        elif move_type == "water" or move_type == "ground" or move_type == "rock":
            effectiveness*=2
    #defending pokemon type 
    if pkm_type1 == "normal" or pkm_type2 == "normal":
        #no effect
        if move_type == "ghost":
            effectiveness *=0
        #super character
        elif move_type == "fighting":
            effectiveness *=2
    #defending pkm type electric
    if pkm_type1 == "electric" or pkm_type2 == "electric":
        #not very effective
        if move_type == "electric" or move_type == "flying" or move_type == "steel":
            effectiveness/=2
        #super effective
        elif move_type == "ground":
            effectiveness*=2
    #defending pokemon grass
    if pkm_type1 == "grass" or pkm_type2 == "grass":
        #not very effective moves
        if move_type == "water" or move_type == "electric" or move_type == "grass" or move_type == "ground":
            effectiveness/=2
        elif move_type == "fire" or move_type == "ice" or move_type == "poison" or move_type == "flying" or move_type == "bug":
            effectiveness*=2
    #defending pokemon ice
    if pkm_type1 == "ice" or pkm_type2 == "ice":
        #not very effective moves
        if move_type == "ice":
            effectiveness/=2
        #super effective moves
        elif move_type == "fire" or move_type == "fighting" or move_type == "rock" or move_type == "steel":
            effectiveness*=2
    #defending pokemon fighting
    if pkm_type1 == "fighting" or pkm_type2 == "fighting":
        #not very effectiv moves
        if move_type == "bug" or move_type == "rock" or move_type == "dark":
            effectiveness/=2
        #super effectvie move types
        elif move_type == "flying" or move_type == "psychic":
            effectiveness*=2
    #defending pokemon type poison
    if pkm_type1 ==  "poison" or pkm_type2 == "poison":
        #not very effective moves
        if move_type == "grass" or move_type == "fighting" or move_type == "poison" or move_type == "bug":
            effectiveness/=2
        elif move_type == "ground" or move_type == "psychic":
            effectiveness*=2
    #defending pokmeon ground
    if pkm_type1 == "ground" or pkm_type2 == "ground":
        #no effect moves
        if move_type == "electric":
            effectiveness*=0
        #not very effective types
        elif move_type == "poision" or move_type == "rock":
            effectiveness/=2
        #super effective types
        elif move_type == "water" or move_type == "grass" or move_type == "ice":
            effectiveness*=2
    #defending pokemon flying
    if pkm_type1 == "flying" or pkm_type2 == "flying":
        #no effect types
        if move_type == "ground":
            effectiveness*=0
        #not very effective types
        elif move_type == "grass" or move_type == "fighting" or move_type == "bug":
            effectiveness/=2
        #super effective types
        elif move_type == "electric" or move_type == "ice" or move_type == "rock":
            effectiveness*=2
    #defending pokmeon psychic
    if pkm_type1 == "psychic" or pkm_type2 == "psychic":
        if move_type == "fighting" or move_type == "psychic":
            effectiveness/=2
        elif move_type == "bug" or move_type == "ghost" or move_type == "dark":
            effectiveness*=2
    #defending pokemon bug
    if pkm_type1 == "bug" or pkm_type2 == "bug":
        if move_type == "grass" or move_type == "fighting" or move_type == "ground":
            effectiveness/=2
        elif move_type == "fire" or move_type == "flying" or move_type == "rock":
            effectiveness*=2
    #defending pokemon rock
    if pkm_type1 == "rock" or pkm_type2 == "rock":
        #move type not very effective
        if move_type == "normal" or move_type == "fire" or move_type == "poison" or move_type == "flying":
            effectiveness/=2
        #move type super effective 
        elif move_type == "water" or move_type == "grass" or move_type == "fighting" or move_type == "ground" or move_type == "steel":
            effectiveness*=2
    #defending pokemon ghost
    if pkm_type1 == "ghost" or pkm_type2 == "ghost":
        #no effect 
        if move_type == "normal" or move_type == "fighting":
            effectiveness*=0
        #nit very effective
        elif move_type == "poison" or move_type == "bug":
            effectiveness/=2
        #super effective move types
        elif move_type == "ghost" or move_type == "dark":
            effectiveness*=2
    #defending pokemon dragon
    if pkm_type1 == "dragon" or pkm_type2 == "dragon":
        #not very effective move types
        if move_type == "fire" or move_type == "water" or move_type == "grass":
            effectiveness/=2
        #super effective move types
        elif move_type == "ice" or move_type == "dragon":
            effectiveness*=2
    #defending pokemon dark
    if pkm_type1 == "dark" or pkm_type2 == "dark":
        #no effect
        if move_type == "psychic":
            effectiveness*=0
        #not very effective move types
        elif move_type == "ghost" or move_type == "dark":
            effectiveness/=2
        #super effective move types
        elif move_type == "fighting" or move_type == "bug":
            effectiveness*=2
    if pkm_type1 == "steel" or pkm_type2 == "steel":
        #no effect move types
        if move_type == "poison":
            effectiveness*=0
        #not very effective move types
        elif move_type == "normal" or move_type == "grass" or move_type == "ice" or move_type == "flying" or move_type == "psychic" or move_type == "bug" or move_type == "rock" or move_type == "dragon" or move_type == "steel":
            effectiveness/=2
        #super effective move types
        elif move_type == "fire" or move_type == "fighting" or move_type == "ground":
            effectiveness*=2

    return effectiveness

#returns 1 if move hits, 0 if move misses
def roll_accuracy(move):
    if move.get_accuracy() == 100:
        return True
    elif (random.randint(0, 100)) <= move.get_accuracy():
        return True
    else:
        return False
    
#this function waits for 5 seconds in a different thread so that the screen keeps rendering
def thread_wait():
    time.sleep()


''' for testing only
def main():
    pokemon_bag = [pokemon_objects.bulbasaur, pokemon_objects.charazard]

    trainer1 = Character("Ash", pokemon_bag, [], 1000,
                              "I'm on a journey to become a Pokemon Master!")

    trainer2 = Character("Misty", pokemon_bag, [], 800, "Water types are the best!")

'''