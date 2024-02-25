import numpy as np 
# removed raise and all-in will implement later
#may need to optimize by using non numpy arrays supposviely really slow 
class InformationSet():
    def __init__(self,key):
      
        self.playable = len(currently_playable(key))
        self.key = key
        self.regret_sum = np.zeros(self.playable)
        self.strategy_sum = np.zeros(self.playable)
        self.strategy = np.repeat(1/self.playable,self.playable)
        self.reach_pr = 0
        self.reach_pr_sum = 0

    def next_strategy(self):
        self.strategy_sum += self.reach_pr*self.strategy
        self.strategy = self.calc_strategy()
        self.reach_pr_sum += self.reach_pr
        self.reach_pr = 0
    
    def calc_strategy(self):
        """
        Calculate current strategy from sum of regrets.
        """
        strategy = self.make_positive(self.regret_sum)
        total = sum(strategy)
        if total > 0:
            strategy = strategy / total
        else:
            n = self.playable
            strategy = np.repeat(1/n,n)
        
        return strategy
    
    def get_average_strategy(self):
        strategy = self.strategy_sum/self.reach_pr_sum

        #clean up actions
        strategy = np.where(strategy < 0.001,0,strategy)

        total = sum(strategy)
        strategy /= total

        return strategy

    def make_positive(self,x):
        return np.where(x>0,x,0)

    #( this is a copy paste from knuh, since it mostly the same)
    def __str__(self):
        strategies = ['{:03.2f}'.format(x) for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)
    
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
            return ['p','a','f']
        if history[-1] == 'p':
            if history.count('p') < 2:
                return ['p','a','f']
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
