from tqdm import tqdm
import eval7
import numpy as np
import pickle
Rank = "2346789TJKQA"
Suits = "shdc"

with open("marco_abstraction/output_files/pickle_files/computed_distances.pickle",'rb') as hand_dict_file:
    hand_dict = pickle.load(hand_dict_file)

with open("marco_abstraction/output_files/pickle_files/computed_distances_canon.pickle",'rb') as canon_dict_file:
    canon_dict = pickle.load(canon_dict_file)

with open("marco_abstraction/output_files/pickle_files/computed_centers.pickle",'rb') as canon_dict_file:
    center_dict = pickle.load(canon_dict_file)

def kmeanspp(data,centers,canon_cards):
    """
    centers = np.array([[tuple(floats)]])
    data = np.array([[tuple(floats)]])
    """
    buckets = {i: [] for i in range(len(centers))} # equities
    canonical_buckets = {i: [] for i in range(len(centers))} # actual cards on board
    print("kmeanspp")
    for data_point in tqdm(range(len(data))):
        distances = np.array([np.linalg.norm(np.array(data[data_point]) - np.array(center)) for center in centers])
        min_index = np.argmin(distances)
        buckets[min_index].append(data[data_point])
        canonical_buckets[min_index].append(canon_cards[data_point])
    return buckets,canonical_buckets

all_buckets = {}
stored_canonical_buckets = {}
for hand in hand_dict:
    bucket,canon_bucket = kmeanspp(hand_dict[hand],center_dict[hand],canon_dict[hand])
    all_buckets[hand] = bucket
    stored_canonical_buckets[hand] = canon_bucket

with open("marco_abstraction/output_files/pickle_files/computed_flop_buckets.pickle","wb") as flop_buckets_pickle:
    pickle.dump(all_buckets,flop_buckets_pickle)

with open("marco_abstraction/output_files/pickle_files/computed_flop_canon_buckets.pickle","wb") as flop_canon_buckets_pickle:
    pickle.dump(stored_canonical_buckets,flop_canon_buckets_pickle)

with open("marco_abstraction/output_files/computed_buckets.txt",'a') as comp_buck:
    for key in stored_canonical_buckets:
        print(key, file = comp_buck)