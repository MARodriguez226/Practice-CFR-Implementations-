SD_flops = []
SD_flop_dict = {}
import eval7
n_cards = [2,3,4,5,6,12,13,14,15,16,22,23,24,25,26,32,33,34,35,36]

#basic non-optimized isomorphism algos

def make_flops(player_hand,opp_hand):
    """
    11/6/23 unfinished
    returns all the possible flops given the cards at play.
    """
    possible_num = n_cards.copy()
    #possible_num = [2,3,4,5,12,13,14,15]
    #need to optimize this 
    for num in player_hand:
        if num in possible_num:
            possible_num.remove(num)
    for num in opp_hand:
        if num in possible_num:
            possible_num.remove(num)
    
    flops = []
    for i in possible_num:
        for j in possible_num:
            for k in possible_num:
                if i != k and i !=j and j!= k and tuple(sorted((i,j,k))) not in flops:
                    flops.append(tuple(sorted((i,j,k))))
    
    return flops


def make_starting_hand():
    #working
    hand_set = set()
    possible_num =n_cards.copy()
    for i in possible_num:
        for j in possible_num:
            if i!=j :
                #ensures no double counting
                hand_set.add(tuple(sorted([i,j])))
    
    return hand_set

def make_all_flops():
    """
    11/6/23 unfinished
    returns all the possible flops given the cards at play.
    """
    possible_num = n_cards.copy()

    flops = []
    for i in possible_num:
        for j in possible_num:
            for k in possible_num:
                if i != k and i !=j and j!= k and tuple(sorted((i,j,k))) not in flops:
                    flops.append(tuple(sorted((i,j,k))))
    
    return flops
sd_sh = make_starting_hand()
all_flops = make_all_flops()
def starting_hand_iso(hand):
    #hand_iso = set()
    new_hand = []
    #count 
    #suit_count = {'s': 0,'h':0,'d':0,'c':0}
    suit_count = [0,0,0,0]
    for card in hand:
        suit_count[card//10] += 1
    sorted_count = sorted(suit_count,key = lambda x: -x)

    cards_counted = 0
    suit = 0
    while cards_counted < 2:
        #print(suit_count)
        index = suit_count.index(sorted_count[suit])
        cards_counted += suit_count[index] 
        suit_count[index] = 0

        for card in hand:
            if card//10 == index:

                new_hand.append(suit*10 + card - card//10 * 10)    

        suit += 1
    return tuple(new_hand)

iso_starting_hands = set()
for hand in sd_sh:
    iso_starting_hands.add(starting_hand_iso(hand))

def make_flop_iso(hand):
    #hand_iso = set()
    new_hand = [0,0,0,0,0]
    #count 
    #suit_count = {'s': 0,'h':0,'d':0,'c':0}
    suit_count = [0,0,0,0]
    for card in hand:
        suit_count[card//10] += 1
    sorted_count = sorted(suit_count,key = lambda x: -x)

    cards_counted = 0
    suit = 0

    while cards_counted < 5:
        #print(suit_count)
        index = suit_count.index(sorted_count[suit])
        cards_counted += suit_count[index] 
        suit_count[index] = 0

        for card in range(len(hand)):
            if hand[card]//10 == index:

                new_hand[card] = suit*10 + hand[card] -hand[card]//10 * 10   

        suit += 1
    return new_hand

flop_isos = set(((12,13,14),(13,14,15),(14,15,16),(12,14,15),(12,15,16),(12,13,15),(12,13,16),(12,14,16),(13,14,16)))
#iso_starting_hands = set()
for sh in iso_starting_hands:
    for flop in all_flops:
        iso = make_flop_iso(sh+flop)
        if len(set(iso)) == 5:
            flop_isos.add(tuple(iso[2:]))
   