import math
import numpy as np
import random
from copy import deepcopy as copy
from Settings import*

def neighbour(neighbours,sol,i,d,sign):
    if isBetween(sol[i]+STEP_SIZE[i]*sign,d): 
                neighbour = copy(sol)
                neighbour[i]+=STEP_SIZE[i]*sign
                neighbours.append(neighbour)

class Optimizer:
    def __init__(self, cost_fn, start_sol=np.array([0,0,90]), domains = np.array([0.5,5,5])):
        self.cost_fn = cost_fn
        self.best_sol = self.sol = start_sol
        self.best_profit = self.profit = cost_fn(start_sol)
        self.domains = domains
        self.isRunning = True
    
    def neighbours_fn(self,domains, sol):
        neighbours = []
        for i, d in enumerate(domains):
            neighbour(neighbours,sol,i,d,+1)
            neighbour(neighbours,sol,i,d,-1)
        return neighbours

class SA(Optimizer):
    def __init__(self, cost_fn, start_sol, domains, T=DEFAULT_SA_TEMPERATURE, cool_factor = 0.995):
        super().__init__(cost_fn,start_sol,domains)
        self.T = T
        self.cool_factor = cool_factor
        self.best_E=self.Ea=self.best_profit

    def step(self):
        """Get next solution"""
        found = False
        neighbours = self.neighbours_fn(self.domains, self.sol)
        next_sol = random.choice(neighbours)
        """Calculate next energy"""
        Eb = self.cost_fn(next_sol)
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
                found = True
        # Decrease temperature
        self.T = self.cool_factor * self.T
        return found

    def hasFinished(self):
        return self.T<=1

    def getSol(self):
        return self.best_sol
    
    def status(self):
        return ("SA Optimizer temperature : {}".format(round(self.T,1)))

class TS(Optimizer):

    def __init__(self, cost_fn, start_sol, domains, max_it=DEFAULT_TS_ITERATIONS):
        super().__init__(cost_fn,start_sol,domains)
        self.max_it = max_it
        self.explored=[start_sol]
        self.explored_profit=[cost_fn(start_sol)]
        self.it=0

    def step(self):
        found=False
        if self.it < self.max_it:
            #Find not explored neighbours
            neighbours = self.neighbours_fn(self.domains, self.sol)
            unexplored = [neighbour for neighbour in neighbours if neighbour not in self.explored]
            #Choose an unexplored neighbour randomly
            if(unexplored):
                self.sol=random.choice(unexplored)
                self.profit=self.cost_fn(self.sol)
            #If no neighbours unexplored
            else:
                #Get the explored neighbour with the best profit from memory
                indexes = [self.explored.index(x) for x in neighbours]
                profits = [self.explored_profit[i] for i in indexes]
                best_index = profits.index(max(profits))
                self.sol = neighbours[best_index]
                self.profit = profits[best_index]
            #Update the profit if a better solution is found
            if (self.profit > self.best_profit):
                self.best_sol, self.best_profit = self.sol, self.profit
                found = True
            #Insert solution in the explored list
            self.explored.append(self.sol)
            self.explored_profit.append(self.profit)
            self.it+=1
        return found

    def hasFinished(self):
        return self.it >= self.max_it

    def getSol(self):
        return self.best_sol

    def status(self):
        return 'TS Optimizer iterations: {}'.format(self.max_it-self.it)