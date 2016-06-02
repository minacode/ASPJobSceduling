from abc import *
import random
import math

random.seed()

class Problem(metaclass=ABCMeta):
    @abstractmethod
    def evaluate(item):
        pass
        
    @abstractmethod
    def get_neighbours(item):
        pass
        
    @abstractmethod
    def get_neighbour(item):
        pass
        
    @abstractmethod
    def get_initial_state():
        pass
    
    @abstractmethod
    def does_terminate():
        pass
        
    @abstractmethod
    def does_halt():
        pass
        
        
def linear_cooling(T, t):
    if T - t > 0:
        return T - t
    else:
        return 1

def simulated_annealing(T, problem, cooling_ration):
    t = 0
    actual_state = problem.get_initial_state
    actual_eval  = problem.evaluate(actual_state)
    best_state   = actual_state
    best_eval    = problem.evaluate(best_state)
    while not problem.does_halt():
        while not problem.does_terminate():
            neighbour_state = problem.get_neighbour(actual_state)
            neighbour_eval  = problem.evaluate(neighbour_state)
            if actual_eval < neighbour_eval:
                actual_state = neighbour_state
                actual_eval  = neighbour_eval
                if best_eval < actual_eval:
                    best_state = actual_state
                    best_eval  = actual_eval
            elif random.random() < math.exp((actual_eval - neighbour_eval) / T):
                actual_state = neighbour_state
                actual_eval  = neighbour_eval
        T = cooling_ration(T, t)
        t += 1
