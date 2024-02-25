import eval7 as ev
import pickle
from tqdm import tqdm
import random

with open("custom_cfr/game_library/HUNL/HUNL_extras/bucketed_flops (2).pkl",'rb') as computed_flop_buckets_file:
    old_computed_flop_buckets = pickle.load(computed_flop_buckets_file)

with open("custom_cfr/game_library/HUNL/HUNL_extras/bucketed_turns (3).pkl",'rb') as computed_turn_buckets_file:
    old_computed_turn_buckets = pickle.load(computed_turn_buckets_file)

with open("custom_cfr/game_library/HUNL/HUNL_extras/bucketed_rivers (3).pkl",'rb') as computed_river_buckets_file:
    old_computed_river_buckets = pickle.load(computed_river_buckets_file)

ranges = [ev.HandRange('23s,24s,25s,26s,27s,34s,35s,36s,37s,45s,46s,32o,43o,42o,54o,53o,52o,65o,64o,63o,62o,74o,73o,72o,83o,82o,28s,29s,2Ts,38s,39s,47s,48s,49s,75o,85o,84o,95o,94o,93o,92o,T5o,T4o,T3o,T2o,J3o,J2o'),
          ev.HandRange('3Ts,4Ts,56s,57s,58s,59s,5Ts,67s,68s,69s,6Ts,78s,79s,89s,67o,68o,69o,6To,78o,79o,7To,89o,8To'), 
            ev.HandRange('6Qs,7Ts,7Js,7Qs,8Ts,8Js,8Qs,8Ts,9Ts,9Js,9Qs,TJs,T9o,J8o,J9o,JTo,Q8o,Q9o,QTo,QJo'),
            ev.HandRange( '33,44,55,K3s,K4s,K5s,K6s,K7s,K8s,A2s,A3s,A4s,A5s,A6s,K5o,K6o,K7o,K8o,K9o,A2o,A3o,A4o,A5o,A6o,A7o,A8o,22,J2s,J3s,J4s,J5s,J6s,Q2s,Q3s,Q4s,Q5s,K2s,J4o,J5o,J6o,J7o,Q2o,Q3o,Q4o,Q5o,Q6o,Q7o,K2o,K3o,K4o'),
            ev.HandRange('66,77,QTs,QJs,K9s,KTs,KJs,KQs,A7s,A8s,A9s,ATs,AJs,AQs,AKs,KTo,KJo,KQo,A9o,ATo,AJo,AQo,AKo'),
              ev.HandRange('88,99,TT,JJ,QQ,KK,AA')]
preflop_subset = [[2,1],[2, 3], [2, 4], [2, 5], [2, 0],[3,2], [3, 2], [3, 4], [3, 5], [3, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 0],[5,1],[5, 2], [5, 3], [5, 4], [5, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]

curr_key = ""
for key in old_computed_turn_buckets:
    curr_key = key

computed_flop_buckets = {}
for key in tqdm(old_computed_flop_buckets):
    stored_dict = {}
    for bucket in old_computed_flop_buckets[key]:
        stored_dict[bucket] =  [[ev.Card(card) for card in board] for board in old_computed_flop_buckets[key][bucket]]
    
    computed_flop_buckets[key] = stored_dict

computed_turn_buckets = {}
for key in old_computed_turn_buckets:
    stored_dict = {}
    for bucket in old_computed_turn_buckets[key]:
        #print(old_computed_turn_buckets[key][bucket])
        stored_dict[bucket] = [[ev.Card(turn)] for turn in old_computed_turn_buckets[key][bucket]]
    
    computed_turn_buckets[key] = stored_dict

computed_river_buckets = {}
for key in old_computed_river_buckets:
    stored_dict = {}
    for bucket in old_computed_river_buckets[key]:
        stored_dict[bucket] = [[ev.Card(river)] for river in old_computed_river_buckets[key][bucket]]
    
    computed_river_buckets[key] = stored_dict
 
preflop_bucket_dict = {str(i):[] for i in range(1,len(ranges)+1)}
for bucket in range(len(ranges)):
    for hand,w in ranges[bucket].hands:
        if str(hand) in (computed_flop_buckets.keys()):
            preflop_bucket_dict[str(bucket)].append(list(hand))

all_flops = []
for key in computed_flop_buckets:
    for bucket in range(3):
        all_flops.extend(computed_flop_buckets[key][bucket])
    break
all_flops = sorted(list(all_flops), key= lambda x:random.random())[:10]

all_turns = []
for key in computed_turn_buckets:
    for bucket in range(3):
        all_turns.extend(computed_turn_buckets[key][bucket])
    break

all_turns = sorted(list(all_turns), key= lambda x:random.random())[:10]
all_rivers = []
for key in computed_river_buckets:
    for bucket in range(3):
        all_rivers.extend(computed_river_buckets[key][bucket])
    break
all_rivers = sorted(list(all_rivers), key= lambda x:random.random())[:10]