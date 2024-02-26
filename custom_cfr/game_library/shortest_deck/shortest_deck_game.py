from game_library.shortest_deck.shortest_deck_infoset import InformationSet
import math
import eval7
from tqdm import tqdm
from game_library.shortest_deck.sd_extras.SD_preflop_flop_maker import iso_starting_hands,flop_isos
# playable actions for SD,x = check, c = call,b = bet, f = fold, r = raise, a = all-in, removed raise
#all_in addded 
n_cards = [2,3,4,5,6,12,13,14,15,16,22,23,24,25,26,32,33,34,35,36]
stack_size = 200
bet_sizes = [3,1/3,3/4,1.5]
default = ["",-1,-1,1,1,1]
card_dict = {2:'2s',3:'3s',4:'4s',5:'5s',6:'6s',12:'2h',13:'3h',14:'4h',15:'5h',16:'6h',22:'2c',23:'3c',24:'4c',25:'5c',26:'6c',32:'2d',33:'3d',34:'4d',35:'5d',36:'6d'}

def is_chance_node(history):
    """
    determin  es if we are at a chance node on tree

    A chance node occurs when a chance event occurs (e.i. preflop,flop,turn,river,etc)
    
    When does a chance node occur for SD:

        Case 1: Preflop
            In preflop when history == "", no cards have been dealt thus a chance node occurs
        
        Case 2: Flop
            The flop occurs after preflop action is closed (bet-check), and a fold or all-in call did not occur. This happens when history[:-2] 
            contains {c} and 'a' is not in history (this would mean all-in was called, no post flop action nesscary)
    """
    if history == "" or (history[-1] == 'c' and ('a' not in history and '&' not in history) and history[-2:] != 'ac'):
        return True
    else:
        return False
    

    
def is_terminal(history):
    """
    Returns true if the node is a terminal node (game ends)

    A terminal node occurs when there is a terminal action or an action that completely stops the game and thus winner is ready to be decided and payed out

    When does a terminal node occur for SD:

        Case 0: Fold 
            When the player folds during any point of the game and history[:-1] = 'f', we reach a terminal node since no further actions can be taken

        Case 1: Checked Back
            When the player checks back after the flop and history[:-2] = xx, we reach a terminal node since no further actions can be taken by either player

        Case 2: Bet is Called
            When a player calls a bet after the flop and history[-1] = c, we reach a termianl node since no further actions can be taken by either player
        
        Case 3: All-in is called
            When a player calls a all-in bet at any point of the game and history[:-2] = ac, we reach a terminal node since no further actions can be taken by either player

    """

    #some of these should stop to early like 'xx','bc','ac' because these are only terminal sometimes

    if history[-1] == 'f' or (history[-2:] in {'bc','xx','Bc','Oc'} and "&" in history) or history[-2:] == "ac":
        # presumingly 2 cases where we reach a terminal node, a fold occurs (f), or betting closes (bc,ac)
        return True 
    else:
        return False

#hand ranking presumingly works 
def hand_rank(player_hand, opp_hand):
    """
    given some form of hand, return the hand ranking

    returns int(total_ranking) 252 total hands possible
    """
    player_hand = [eval7.Card(card_dict[card]) for card in player_hand]
    opp_hand = [eval7.Card(card_dict[card]) for card in opp_hand]
    return eval7.evaluate(player_hand) > eval7.evaluate(opp_hand)
def currently_playable(history):
    """
    given the history return an array of playable moves

    What are the playable moves for given histories:

        Case 0: Chance Event
            When history[-1] in {?,&}, this means a chance event has occured. If we are preflop (?), we can raise or fold. If we are post-flop (&), we can check or bet.

        Case 1: When History Ends in Bet
            When history[-1] in {b,B}, the actions possible are call,raise,or fold.
        
        Case 2: When History Ends in all-in
            When history[-1] == 'a', the actions possible are call or fold.
        
        Case 3: When History Ends in check
            When history[-1] == 'x', the actions possible are check or bet.

    Note: We should never encounter call when currently_playable is ran since a call would require a chance node or terminal to be evaluated.

    return [n_1,n_2,...,n_i]
    """
    #temporary all-in adjuster
    all_in = True

    if all_in:
        #print(history[-2:])
        if history[-1] == '?':
            return ['p','a','f']
        if history[-1] == 'p':
            if history.count('p') < 2:
                return ['c','p','a','f']
            else:
                return ['c','a','f']
        if history[-1] == '&':
            return ['x','b','B','a','f']
        if history[-1] == 'b':
            return ['c','B','a','f']
        if history[-1] in {'B','O'}:
            return ['c','a','f']
        if history[-1] == 'a':
            return ['c','f']
        if history[-1] == 'x':
            return ['x','b','B','a','f']
    else:
        # no all-in feature 
        if history[-1] == '?':
            return ['B','f']
        if history[-1] == '&':
            return ['b','B','f']
        if history[-1] == 'b':
            return ['c','B','f']
        if history[-1] == 'B':
            return ['c','f']
        if history[-1] == 'x':
            return ['x','b','B','f']

def stack_change(action,is_player_1,player_1_stack,player_2_stack):
    """
    given an action returns the change in players stack size

    How do stacks change for a given action:

        Case  0: Player Folds
            When a player folds, action = 'f' and stack sizes do not change.
        
        Case 1: Player Checks
            When a player checks, action = 'x' and stack sizes do not chance

        Case 2: Player Bets
            When a player bets, action in {b,B,a} and stack sizes chance as such:
                WLOG assume player 2 places a bet, return (player_1_stack, player_2_stack - bet)    

        Case 3: Player Calls
            When a player calls, action = 'c' and stack sizes change as such:
                WLOG assume player 1 calls a bet, return (player_1_stack - bet, player_2_stack) 
        
        
        
    returns (player_1_stack, player_2_stack)
    """
    pot = 2*stack_size - player_1_stack - player_2_stack
    p_size,b_size,B_size,O_size = bet_sizes
    bet_dict = {'b':pot*b_size,"B":pot*B_size,'p':p_size*pot,'O':O_size}


    if is_player_1:
        call = player_1_stack - player_2_stack
        if action == 'f':
            return (player_1_stack,player_2_stack)
        if action == 'x':
            return (player_1_stack,player_2_stack)
        if action in {'b','B','p','O'}:
            return (player_1_stack - bet_dict[action],player_2_stack)
        if action == 'a':
            return (player_1_stack-player_1_stack, player_2_stack)
        if action == 'c':
            return (player_1_stack - call, player_2_stack)
    else:
        call = player_2_stack - player_1_stack
        if action == 'f':
            return (player_1_stack,player_2_stack)
        if action == 'x':
            return (player_1_stack,player_2_stack)
        if action in {'b','B','p','O'}:
            return (player_1_stack,player_2_stack - bet_dict[action])
        if action == 'a':
            return (player_1_stack, player_2_stack - player_2_stack)
        if action == 'c':
            return (player_1_stack, player_2_stack - call)

    
def terminal_util(history,player_1,player_2,player_1_stack,player_2_stack):
    """
    history str: some valid string composed of {c,x,r,f,a}

    player_1 int: hand of player 1
    player_2 int: hand of player 2
    player_1_stack: the number of chips player 1 has
    player_2_stack: the number of chips player 2 has
    
    returns the utility once we are at a terminal node/what is the outcome of the game
    """
    n = len(history)
    card_player = player_1 if n%2 == 0 else player_2
    card_opp = player_2 if n%2 == 0 else player_1
    
    pot = 2*stack_size - player_1_stack - player_2_stack
    
    #all-in equity computed as the EV of hands on all flops
    if history[-2:] == 'ac' and "&" not in history:
        flops = flop_isos
        ev_pot = 0
        for flop in flops:
          ev_pot += pot/2 if hand_rank(card_player  + flop,card_opp + flop) else -pot/2
        
        return ev_pot/len(flops)
    
    
    if history[-1]  == 'f':
        return 0
    elif history[-1] == 'c' or history[-1] == 'x':
        #when the opponet calls or checks we must look at showdown to determine pot util
        return pot/2 if hand_rank(card_player,card_opp) else -pot/2
    
def chance_util(func,i_map,history,i,j,pr_1,pr_2,pr_c,player_1_stack,player_2_stack):
    """
    the utility gained as a result of a chance node, needed to be activated anytime a chance event
    occurs we need to see the exepected value given all chance event outcomes.
    """
    if history == "":
        expected_value = 0
        
        hand_possibilities = len(iso_starting_hands)
        for hero in tqdm(iso_starting_hands):
            for villian in iso_starting_hands:
                if hero != villian:
                    expected_value += func(i_map,'??',hero,villian,1,1,1/hand_possibilities)
        return expected_value / hand_possibilities
    else:
        expected_value = 0
        flop_possibilities = len(flop_isos)
        for flop in flop_isos:
            if i[0] not in flop and j[0] not in flop and i[1] not in flop and j[1] not in flop:

                parity =  '&&' if len(history) % 2 else '&&&'
                expected_value += func(i_map,history + parity , i + flop,j + flop,pr_1,pr_2,1/flop_possibilities*pr_c,player_1_stack,player_2_stack)
        return expected_value/flop_possibilities
    
def card_str(hand):
    """
    turns hand into a str that the infoset can interpret as a key
    tuple hand = (int,int,)
    """
    # we will be using suit rankings spades > hearts
    str_card = ""
    for card in hand:
       
        if card != 0:
            str_card += card_dict[card] + ' '

    return str_card

def get_info_set(i_map,hand,history):
    """
    Retrieves info set from dict
    """
    cards = card_str(hand)
    key = cards + " " + history
    info_set = None
    if key not in i_map:
        info_set = InformationSet(key)
        i_map[key] = info_set
        return info_set
    return i_map[key]

#this definitly works Done 12/24/23
def display_results(ev, i_map):
    with open('custom_cfr/game_library/shortest_deck/sd_strat.txt', 'a') as strat:
        print('player 1 expected value: {}'.format(ev), file=strat)
        print('player 2 expected value: {}'.format(-1 * ev), file=strat)

        print()
        print('player 1 strategies:',file=strat)
        sorted_items = sorted(i_map.items(), key=lambda x: x[0])
        for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
            print(v, file= strat)
        print()
        print('player 2 strategies:', file=strat)
        for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
            print(v, file=strat)
        #print(i_map,file = strat)
    print("in sd_strat.py file")
