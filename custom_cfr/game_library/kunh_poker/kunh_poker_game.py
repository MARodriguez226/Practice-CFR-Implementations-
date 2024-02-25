from game_library.kunh_poker.kunh_infoset import InformationSet

playable_actions = ['c','b']
actions = 2
n_cards = 3
default = ["",-1,-1,1,1,1]

def is_chance_node(history):
    """
    Determine if we are at a chance node on tree
    """
    return history ==""

def chance_util(i_map,func):
    expected_value = 0
    n_possibilities = 6
    for i in range(n_cards):
        for j in range(n_cards):
            if i != j:
                expected_value += func(i_map,'rr',i,j,1,1,1/n_possibilities)
    return expected_value/n_possibilities

def is_terminal(history):
    """
    Returns true if games end
    """
    pos = {'rrcc':True,'rrcbc':True,"rrcbb":True,"rrbc":True,"rrbb":True}
    return history in pos

def terminal_util(history,card_1,card_2):
    """
    Returns the utility of a terminal history.
    """
    n = len(history)
    card_player = card_1 if n%2 == 0 else card_2
    card_opp = card_2 if n%2 == 0 else card_1

    if history == "rrcbc" or history =="rrbc":
        return 1
    elif history == "rrcc":
        return 1 if card_player > card_opp else -1

    assert(history == "rrcbb" or history == "rrbb")
    return 2 if card_player > card_opp else -2

def card_str(card):
    if card == 0:
        return "J"
    elif card == 1:
        return "Q"
    return "K"

def get_info_set(i_map,card,history):
    """
    Retrieve info set from dic
    """
    key = card_str(card) + " " + history
    info_set = None

    if key not in i_map:
        info_set = InformationSet(key)
        i_map[key] = info_set
        return info_set
    
    return i_map[key]



def display_results(ev, i_map):
    print('player 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))

    print()
    print('player 1 strategies:')
    sorted_items = sorted(i_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print()
    print('player 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)