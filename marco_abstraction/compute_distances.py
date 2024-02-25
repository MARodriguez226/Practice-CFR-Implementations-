from txt_files.abstr_extras import ranges
from txt_files.boards import boards,pre_map_boards
from txt_files.turn_hands import mapped_hands,hand_dict,canon_dict
from tqdm import tqdm
import eval7
import numpy as np
import pickle

Rank = "2346789TJKQA"
Suits = "shdc"

def compute_distances(hand_list,board_list):
    """
    hands = eval7.Card(x)
    boards = eval7.Card(x)

    hand_dict[(card_1,card_2)]: (value)
    cannon_dict[(card_1,card_2)]: (cards)
    """
    print('here compute distances')
    distances = []
    for i in tqdm(range(len(hand_list))):
        point = ()
        for bucket in ranges:
            villain = bucket
            equity = eval7.py_hand_vs_range_monte_carlo(hand_list[i],villain,boards[i],300)
            point += (equity,)
        hand_dict[str(hand_list[i])].append(point) # string of hand : equity
        canon_dict[str(hand_list[i])].append(pre_map_boards[i]) # actual cards on board (string of hand : board)
        distances.append(point)
    return distances

distances = compute_distances(mapped_hands,boards)
with open("marco_abstraction/output_files/pickle_files/turn_computed_distances.pickle",'wb') as pickled_file:
    pickle.dump(hand_dict,pickled_file)

with open("marco_abstraction/output_files/pickle_files/turn_computed_distances_canon.pickle","wb") as canon_pickle:
    pickle.dump(canon_dict,canon_pickle)