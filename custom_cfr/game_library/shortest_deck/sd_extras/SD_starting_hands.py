#since we are using all 4-suits we are able to create isomorphism 
#will use the metric that Spades>Hearts>Diamonds>Clubs and normalize the suits we have to these where
#the one that appears the most gets assigned to Spades and 2nd most to Hearts, etc
from SD_preflop_flop_maker import iso_starting_hands,flop_isos
card_dict = {2:'2s',3:'3s',4:'4s',5:'5s',6:'6s',12:'2h',13:'3h',14:'4h',15:'5h',16:'6h',22:'2c',23:'3c',24:'4c',25:'5c',26:'6c',32:'2d',33:'3d',34:'4d',35:'5d',36:'6d'}
starting_hands = iso_starting_hands
flops = flop_isos

