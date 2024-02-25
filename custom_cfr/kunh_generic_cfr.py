#A generic CFR in order to solve for nash equilibrium in any game.
import numpy as np 
from game_library.kunh_poker.kunh_poker_game import *

#recommended of later optimizations that we do not use numpy

#the number of actions that could be taken, n_cards is the number of different cards
default_history,default_p1,default_p2,default_pr_1,default_pr_2,default_pr_c = default
def main():
    """
    Runs iterations of CFR
    """

    i_map = {} # infomation set 
    n_iterations = 10000
    excepted_value = 0

    for _ in range(n_iterations):
        #inital call of the cfr algorithm
        excepted_value += cfr(i_map)
        for _,v in i_map.items():
            v.next_strategy()
    
    excepted_value /= n_iterations

    display_results(excepted_value,i_map)

def cfr(i_map,history = default_history,player_1 = default_p1,player_2 =default_p2,pr_1= default_pr_1,pr_2= default_pr_2,pr_c= default_pr_c):
    """
    CFR Algo

    i_map: dict, a dictionary of all our informations sets for a given game

    history = [{'x_i','x_j','x_k'}], str, some str representing the actions of players
    during some game, 
    
    ***should be optimized so histories can be isomorphically clustehand 
    pr_1: (0,1.0) float, the probablility in which player_1 reaches this history
    pr_2: (0,1.0) float, the probability in which player_2 reaches this historyred***

    player_1: int, a unique representation of what cards the player has in their hand
    player_2: int. a unique representation of what cards the player has in their 
    pr_c: (0,1.0) float, the probability of some chance event 
    """
    if is_chance_node(history):
        """
        We check if we are at a point in the game where a 'chance action' happens
        a 'chance action' is any action out side of the players control
        """
        return chance_util(i_map,cfr)
    
    if is_terminal(history):
        """
        We check if we are at a terminal state in a games history, a terminal state
        is one where the game ends and outcomes are shown
        """
        return terminal_util(history,player_1,player_2)
    
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
    
    # a matrix, of shape  actions, computes sounter factual utility per action
    action_utils = np.zeros(actions)

    for i,action in enumerate(playable_actions):
        # playable actions are actioins a player can take for a given game
        next_history = history + action

        if is_player_1:
            action_utils[i] = -1 * cfr(i_map,next_history,player_1,player_2,pr_1*strategy[i],pr_2,pr_c)

        else:
            action_utils[i] = -1 * cfr(i_map,next_history,player_1,player_2,pr_1,pr_2*strategy[i],pr_c)
    
    util = sum(action_utils*strategy)
    regrets = action_utils - util
    if is_player_1:
        info_set.regret_sum += pr_2 *pr_c *regrets
    else:
        info_set.regret_sum += pr_1 * pr_c * regrets
    
    return util

if __name__ == "__main__":
    main()