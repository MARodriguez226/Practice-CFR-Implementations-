import json
import tqdm
import eval7

with open("marco_abstraction/output_files/pickle_files/turnBoards.json",'r') as f:
    print('reading')
    pre_map_boards = json.load(f)
    print('done')

print(pre_map_boards[:5])

boards = []
for board in tqdm.tqdm(pre_map_boards):
    add_tuple = tuple()
    for card in board:
        add_tuple += (eval7.Card(card),)
    boards.append(add_tuple)
print("Boards Initialized Done")