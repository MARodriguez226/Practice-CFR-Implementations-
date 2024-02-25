#A generic CFR in order to solve for nash equilibrium in any game.
import numpy as np 
from game_library.shortest_deck.shortest_deck_game import *
#from game_library.HUNL.HUNL_game import *
import time
from tqdm import tqdm
#How to change games:
#Change the import from game library in order to change what game is being played
#
#Functions to import: is_chance_node,chance_util,is_terminal,terminal_util,get_info_set,display_results
# 
#Variables to import: playable_actions,default,actions
#
#***recommended of later optimizations that we do not use numpy***

#the number of actions that could be taken, n_cards is the number of different cards
default_history, default_p1, default_p2, default_pr_1, default_pr_2, default_pr_c = default

def main():
    """
    Runs iterations of CFR
    """
    start_time = time.time()
    i_map = {} # infomation set 
    n_iterations = 15
    excepted_value = 0

    for _ in tqdm(range(n_iterations)):
        #inital call of the cfr algorithm
        #print('start of the ' + str(_) + ' iter')
        excepted_value += cfr(i_map)
        for _,v in i_map.items():
            v.next_strategy()
        
    excepted_value /= n_iterations

    display_results(excepted_value,i_map)
    print(time.time()-start_time)

def cfr(i_map, history = default_history,player_1 = default_p1, player_2=default_p2, pr_1=default_pr_1, pr_2=default_pr_2, pr_c=default_pr_c, player_1_stack = stack_size-2, player_2_stack=stack_size-1):
    """
    CFR Algo

    i_map: dict, a dictionary of all our informations sets for a given game

    history = [{'x_i','x_j','x_k'}], str, some str representing the actions of players
    during some game, 
    
    ***should be optimized so histories can be isomorphically clustehand 
    pr_1: (0,1.0) float, the probablility in which player_1 reaches this history
    pr_2: (0,1.0) float, the probability in which player_2 reaches this historyred***

    player_1: int, a unique representation of what cards the player has in their hand
    player_2: int. a unique representation of what cards the player has in their hand
    pr_c: (0,1.0) float, the probability of some chance event 
    """
    if is_chance_node(history):
        """
        We check if we are at a point in the game where a 'chance action' happens
        a 'chance action' is any action out side of the players control
        """
        return chance_util(cfr,i_map,history,player_1,player_2,pr_1,pr_2,pr_c,player_1_stack,player_2_stack)
        
    
    if is_terminal(history):
        """
        We check if we are at a terminal state in a games history, a terminal state
        is one where the game ends and outcomes are shown
        """
        return terminal_util(history,player_1,player_2,player_1_stack,player_2_stack)

    
    n = len(history)
    is_player_1 = n%2 == 0

    #gathers the info set for this node
    info_set = get_info_set(i_map,player_1 if is_player_1 else player_2, history)

    # gathers the strategy for this point in game tree
    strategy = info_set.strategy

    #calculates the probability of reach a certain state
    if player_1:
        info_set.reach_pr += pr_1
    else:
        info_set.reach_pr += pr_2
    
    playable = currently_playable(history)
    # a matrix, of shape  actions, computes sounter factual utility per action

    action_utils = np.zeros(len(playable))

    for i,action in enumerate(playable):
        # need to set up which moves are playable when 
        # playable actions are actioins a player can take for a given game
        #next_history = history + action

        #updates the action utilities in action table 
       
        if is_player_1:
                next_history = history + action
                new_player_1_stack,new_player_2_stack = stack_change(action,is_player_1,player_1_stack,player_2_stack)
                action_utils[i] = -1 * cfr(i_map,next_history,player_1,player_2,pr_1*strategy[i],pr_2,pr_c,new_player_1_stack,new_player_2_stack)
        else:
                next_history = history + action
                new_player_1_stack,new_player_2_stack = stack_change(action,is_player_1,player_1_stack,player_2_stack)
                action_utils[i] = -1 * cfr(i_map,next_history,player_1,player_2,pr_1,pr_2*strategy[i],pr_c,new_player_1_stack,new_player_2_stack)
    
    #updates the players regret sum for some given action
    util = sum(action_utils*strategy)
    regrets = action_utils - util
    if is_player_1:
        info_set.regret_sum += pr_2 *pr_c*regrets
    else:
        info_set.regret_sum += pr_1 * pr_c * regrets
    
    return util

if __name__ == "__main__":
    main()