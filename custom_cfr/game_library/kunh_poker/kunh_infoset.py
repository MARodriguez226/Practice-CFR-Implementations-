import numpy as np
actions = 2
class InformationSet():
    def __init__(self,key):
        self.key = key
        self.regret_sum = np.zeros(actions)
        self.strategy_sum = np.zeros(actions)
        self.strategy = np.repeat(1/actions,actions)
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
            n = actions
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

    def __str__(self):
        strategies = ['{:03.2f}'.format(x) for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)