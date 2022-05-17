import math
import numpy as np
import random

class Optimizer:
    def __init__(self,start_sol=np.array([0,0,90]), domains = np.array([0.5,5,5])):
        self.domains = domains
        self.best_sol = self.sol = start_sol
        self.started = False

class SA(Optimizer):
    def __init__(self,start_sol=np.array([0,0,90]),T=1000, cool_factor = 0.995):
        Optimizer.__init__(self,start_sol)
        self.T = T
        self.cool_factor = cool_factor
        self.best_E=self.Ea=0

    def step(self,model2d,next_sol):
        # Calculate next energy
        Eb = model2d.profit
        if (not self.started):
            self.started=True
            self.best_E=self.Ea=Eb
        # Update sol if next_sol has lower cost (p>1)
        # or we pass the probability cutoff
        p =pow(math.e, (self.Ea-Eb)/self.T)
        if (np.random.uniform() < p):
            self.sol = next_sol
            self.Ea = Eb
            # Save the best ever found
            if (Eb > self.best_E):
                self.best_sol = next_sol
                self.best_E = Eb
        # Decrease temperature
        self.T = self.cool_factor * self.T
        # Get the next solution and return it
        neighbours = neighbours_fn(self.domains, self.sol)
        return random.choice(neighbours)

    def hasFinished(self):
        return self.T<0.1

    def getSol(self):
        return self.best_sol


class TS(Optimizer):

    def __init__(self,start_sol=np.array([0,0,90]),max_it=1000,stop_profit=1000):
        Optimizer.__init__(self,start_sol)
        self.max_it = max_it
        tl=[self.best_sol]
        self.best_candidate = self.best_sol
        self.best_profit=-1000
        self.stop_profit=stop_profit
        self.it=0

    def step(self,model2d,next_sol):
        if self.it < self.max_it:
            # Each iteration search for the more profitable neighbor which is not in the tl
            neighbors = neighbours_fn(self.domains, best_candidate)
            best_candidate, best_candidate_profit = None, -np.inf
            while (best_candidate == None):
                # Choose an un-vetoed candidate
                for candidate in neighbors:
                    candidate_profit = profit_fn(candidate)
                    if (candidate not in tl) and (candidate_profit>best_candidate_profit):
                        best_candidate, best_candidate_profit = candidate, candidate_profit
                # If all the neighbors are in the tl
                if (best_candidate == None):
                    # Break stagnation keeping only the second part of the vetoed candidates
                    tl = tl[len(tl)//2:]
            # Update the best_sol, if a better candidate is found
            if (best_candidate_profit > best_profit):
                best_sol, best_profit = best_candidate, best_candidate_profit
            # If we have reach the stop_profit
            if (best_candidate_profit >= self.stop_profit):
                self.it = self.max_it
            # Veto candidate
            tl.append(best_candidate)
        return (best_profit, best_sol)

    def hasFinished(self):
        return self.it >= self.max_it

    def getSol(self):
        return self.best_sol

    pass


def neighbours_fn(domains, sol):
    neighbours=np.array([sol,sol,sol,sol,sol,sol])

    """Rho"""
    neighbours[4][0]+=domains[0]
    
    neighbours[5][0]-=domains[0]
    if neighbours[5][0] <=0:
        neighbours[5][0]+= 2*domains[0]

    """Theta"""
    neighbours[2][1]+=domains[1]
    neighbours[3][1]-=domains[1]

    """Phi"""
    neighbours[0][2]+=domains[2]
    if(neighbours[0][2]>360): neighbours[0][2]-=360
    neighbours[1][2]-=domains[2]
    if (neighbours[1][2]<=0): neighbours[1][2]+=360
    
    return neighbours