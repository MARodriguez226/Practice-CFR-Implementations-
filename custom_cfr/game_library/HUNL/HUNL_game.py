from game_library.HUNL.HUNL_infoset import *
from game_library.HUNL.HUNL_extras.HUNL_buckets import *
import eval7 as ev
from tqdm import tqdm
import random
stack_size = 200
bet_sizes = [1/3,2/3,1,1.5]
default = ["",-1,-1,1,1,1]

def is_chance_node(history):
    """
    determines if we are at a chance node on tree

    A chance node occurs when a chance event occurs (e.i. preflop,flop,turn,river,etc)
    
    When does a chance node occur for SD:

        Case 1: Preflop
            In preflop when history == "", no cards have been dealt thus a chance node occurs
        
        Case 2: Flop
            The flop occurs after preflop action is closed (bet-call,check-check), and a fold or all-in call did not occur. This happens when history[:-2] 
            contains {c} and 'a' is not in history (this would mean all-in was called, no post flop action nesscary)
        
        Case 3: Turn 
            The turn occurs after flop action is closed (check-check,bet-call), and a fold or all-in call did not occur. This happens when history[-2:] == 'xx', 'bc', and 'a' not in history 
            and & in history.

        Case 4: River
            The river occurs after turn action closed (check-check,bet-call), and a fold or all-in call did not occur.This happens when history[-2:] == 'xx', 'bc', and 'a' not in history 
            and # in history.
    """
    if history == "" or ((history[-1] == 'c' or history[-2:] == 'xx') and history[-2:] != 'ac' and "#" not in history):
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

    if history[-1] == 'f' or (history[-2:] in {'bc','xx','Bc','Pc','Oc'} and "#" in history) or history[-2:] == "ac":
        # presumingly 2 cases where we reach a terminal node, a fold occurs (f), or betting closes (bc,ac)
        return True 
    else:
        return False

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
        if history[-1] == '?':
            return ['B','a','f']
        if history[-1] in {'&','@','#'}:
            return ['x','b','B','a']
            # return ['x','b','B','P','O','a']
        if history[-1] == 'b':
            return ['c','B','a','f']
            # return ['c','B','P','O','a','f']
        if history[-1] in {'B','P','O'}:
            return ['c','a','f']
        if history[-1] == 'a':
            return ['c','f']
        if history[-1] == 'x':
            return ['x','b','B','a']
            #return ['x','b','B','P','O','a']
    # else:
    #     # no all-in feature 
    #     if history[-1] == '?':
    #         return ['B','f']
    #     if history[-1] == '&':
    #         return ['b','B','f']
    #     if history[-1] == 'b':
    #         return ['c','B','f']
    #     if history[-1] == 'B':
    #         return ['c','f']
    #     if history[-1] == 'x':
    #         return ['x','b','B','f']

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
    b_size,B_size,P_size,O_size = bet_sizes
    b_bet = pot*b_size
    B_bet = pot*B_size
    P_bet = pot*P_size
    O_bet = pot*O_size
    if is_player_1:
        call = player_1_stack - player_2_stack
        if action == 'f':
            return (player_1_stack,player_2_stack)
        if action == 'x':
            return (player_1_stack,player_2_stack)
        if action == 'b':
            return (player_1_stack - b_bet,player_2_stack)
        if action == 'B':
            return (player_1_stack - B_bet,player_2_stack)
        if action == 'P':
            return (player_1_stack - P_bet,player_2_stack)
        if action == 'O':
            return (player_1_stack - O_bet,player_2_stack)
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
        if action == 'b':
            return (player_1_stack,player_2_stack - b_bet)
        if action == 'B':
            return (player_1_stack,player_2_stack - B_bet)
        if action == 'P':
            return (player_1_stack,player_2_stack - P_bet)
        if action == 'O':
            return (player_1_stack,player_2_stack - O_bet)
        if action == 'a':
            return (player_1_stack, player_2_stack - player_2_stack)
        if action == 'c':
            return (player_1_stack, player_2_stack - call)

def hand_rank(player_hand, opp_hand):
    """
    given some form of hand, return the hand ranking

    returns int(total_ranking) 252 total hands possible
    """

    return ev.evaluate(player_hand) > ev.evaluate(opp_hand)

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

    if history[-2:] == 'ac' and "#" not in history:
        if "&" not in history:
            p1_whole_cards,p2_whole_cards = card_player.split()[0],card_opp.split()[0]
            #print(p1_whole_cards,p2_whole_cards,"all in pure")
            p1_canonical_hc,p2_canonical_hc = [x for x in ranges[int(p1_whole_cards)].hands[:2]],[x for x in ranges[int(p2_whole_cards)].hands[:2]]
    
            utility = 0
            total_combos = 0

            for p1_canon,p2_canon in zip(p1_canonical_hc,p2_canonical_hc):
                for flop in all_flops:
                    for turn in all_turns:
                        for river in all_rivers:
                            board = flop + turn + river
                            utility += pot/2 if hand_rank(list(p1_canon[0]) + board,list(p2_canon[0]) + board) else -pot/2
                            total_combos += 1

            return utility/total_combos
            
        elif "@" not in history:
            p1_whole_cards,p_flop = card_player.split()
            p2_whole_cards,p_flop = card_opp.split()

            p1_canonical_hc,p2_canonical_hc = [x for x in ranges[int(p1_whole_cards)].hands[:2]],[x for x in ranges[int(p2_whole_cards)].hands[:2]]
    
            players_hand = str(tuple(random.choice(p1_canonical_hc)))
            players_canon_flops = computed_flop_buckets[int(p1_whole_cards)][int(p_flop)] if len(computed_flop_buckets[int(p1_whole_cards)][int(p_flop)]) < 20 else sorted(computed_flop_buckets[int(p1_whole_cards)][int(p_flop)],key = lambda x: random.random())[:10]  

            utility = 0
            total_combos = 0

            for p1_canon,p2_canon in zip(p1_canonical_hc,p2_canonical_hc):
                for flop in players_canon_flops:
                    for turn in all_turns:
                        for river in all_rivers:
                            board = flop + turn + river
                            utility += pot/2 if hand_rank(list(p1_canon[0]) + board,list(p2_canon[0]) + board) else -pot/2
                            total_combos += 1
                            
            return utility/total_combos

        else:
            p1_whole_cards, p_flop,p_turn = card_player.split()
            p2_whole_cards, p_flop,p_turn = card_opp.split()

            p1_canonical_hc,p2_canonical_hc = [x for x in ranges[int(p1_whole_cards)].hands[:2]],[x for x in ranges[int(p2_whole_cards)].hands[:2]]
            players_hand = str(tuple(random.choice(p1_canonical_hc)))
            players_canon_flops = computed_flop_buckets[int(p1_whole_cards)][int(p_flop)] if len(computed_flop_buckets[int(p1_whole_cards)][int(p_flop)]) < 20 else sorted(computed_flop_buckets[int(p1_whole_cards)][int(p_flop)],key = lambda x: random.random())[:10]  


            players_canon_turns = computed_turn_buckets[(int(p1_whole_cards),int(p_flop))][int(p_turn)][:5]
            
            utility = 0
            total_combos = 0

            for p1_canon,p2_canon in zip(p1_canonical_hc,p2_canonical_hc):
                for flop in players_canon_flops:
                    for turn in players_canon_turns:
                        for river in all_rivers:
                            board = flop + turn + river
                            utility += pot/2 if hand_rank(list(p1_canon[0]) + board,list(p2_canon[0])+ board) else -pot/2
                            total_combos += 1
                            
            return utility/total_combos
    
    if history[-1]  == 'f':
        return 0

    p1_whole_cards, p_flop,p_turn,p_river = card_player.split()
    p2_whole_cards, p_flop,p_turn,p_river = card_opp.split()

    p1_canonical_hc,p2_canonical_hc = [x for x in ranges[int(p1_whole_cards)].hands[:2]],[x for x in ranges[int(p2_whole_cards)].hands[:2]]
    
    players_canon_flops = computed_flop_buckets[int(p1_whole_cards)][int(p_flop)] if len(computed_flop_buckets[int(p1_whole_cards)][int(p_flop)]) < 20 else sorted(computed_flop_buckets[int(p1_whole_cards)][int(p_flop)],key = lambda x: random.random())[:10]  


    players_canon_turns = computed_turn_buckets[(int(p1_whole_cards),int(p_flop))][int(p_turn)][:5]
    players_canon_river = computed_river_buckets[(int(p1_whole_cards),int(p_flop),int(p_turn))][int(p_river)][:5]
    
    if history[-1] == 'c' or history[-1] == 'x':
        #print(history[-1],'is call?')
        
        utility = 0
        total_combos = 0
        for p1_canon,p2_canon in zip(p1_canonical_hc,p2_canonical_hc):
            for flop in players_canon_flops:
                for turn in players_canon_turns:
                    for river in players_canon_river:
                        
                        board = flop + turn + river
                        utility += pot/2 if hand_rank(list(p1_canon[0]) + board,list(p2_canon[0]) + board) else -pot/2
                        total_combos += 1
        
                            #when the opponet calls or checks we must look at showdown to determine pot util
        return utility/total_combos

def chance_util(func,i_map,history,i,j,pr_1,pr_2,pr_c,player_1_stack,player_2_stack):
    """
    the utility gained as a result of a chance node, needed to be activated anytime a chance event
    occurs we need to see the exepected value given all chance event outcomes.

    Preflop Criterion: no actions played history = "".

    Flop Criterion: preflop action ended with no all-in preflop.

    Turn Criterion: flop action ended with no all-in flop.

    River Criterion: river action ended with no all-in on the turn.

    """
    if history == "":
        preflop_ev = 0
        for hands in tqdm(preflop_subset):
            player_1, player_2 = hands
            preflop_ev += func(i_map,'??',str(player_1),str(player_2),pr_1,pr_2,1/len(preflop_subset))
        return preflop_ev/len(preflop_subset)

    elif history[-1] in {'c','x'} and "&" not in history:
        flop_ev = 0
        
        # rand_hand = random.choice(preflop_bucket_dict[i])
        #print(i,"players hand")
        flop_set = computed_flop_buckets[int(i)]

        for flop in tqdm(flop_set) :
            parity =  '&&' if len(history) % 2 else '&&&'
            flop_ev += func(i_map,history + parity,str(i) + " "+ str(flop),str(j) + " "+str(flop),pr_1,pr_2,pr_c*1/len(flop_set))
        return flop_ev/len(flop_set)
    
    elif "@" not in history:
        turn_ev = 0
        card1,card2 = i.split()
        turn_subset = computed_turn_buckets[(int(card1),int(card2))]
        for turn in turn_subset:
            parity =  '@@' if len(history) % 2 else '@@@'
            turn_ev += func(i_map,history + parity,i + " "+str(turn),j + " "+str(turn),pr_1,pr_2,pr_c*1/len(turn_subset))
        return turn_ev/len(turn_subset)
    
    elif "#" not in history:
        river_ev = 0
        bucket_1,bucket_2,bucket_3 = i.split()
        river_subset = computed_river_buckets[(int(bucket_1),int(bucket_2),int(bucket_3))]
        parity =  '##' if len(history) % 2 else '###'
        for river in river_subset:
            river_ev += func(i_map,history + parity,i +" "+ str(river),j + " "+str(river),pr_1,pr_2,pr_c*1/len(river_subset))
        return river_ev/len(river_subset)            
    
def card_str(hand):
    """
    turns hand into a str that the infoset can interpret as a key
    tuple hand = (int,int,)
    """
    # we will be using suit rankings spades > hearts
    str_card = ""
    for card in hand:
        str_card += card + ' '
        # if card != 0:
        #     str_card += card_dict[card] + ' '

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

def is_conflict(p1_hand,p2_hand,flop,turn,river):
    """ 
    given a specfic hand,flop,turn,and river, check if there is any conflicting cards. Cards that conflict are cards that appear more than once on the flop turn and/or river.
    """
    return False

def display_results(ev, i_map):
    with open('custom_cfr/game_library/HUNL/HUNL_strat.txt', 'a') as strat:
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
    print("in HUNL_strat.py file")
