import numpy as np
from scipy.optimize import linprog

class LinearProgram(object):
    """A flexing, adaptive linear program."""
    def __init__(self):
        pass # TODO
        # self.
    
    # TODO add analysis tools for MIT class? e.g., report on if your current program is valid

class Scheduler(object):
    def __init__(self):
        self.events = list() # len = num_states
        self.constraints = dict() # len = num_constraints
        
    def addConstraint(self, eventA, eventB, BminusA):
        self.constraints[(eventA, eventB)] = BminusA
        if not eventA in self.events:
            self.events.append(eventA)
        if not eventB in self.events:
            self.events.append(eventB)
        
    def removeConstraint(self, eventA, eventB, BminusA):
        
        pass # TODO
    
    def getSchedule(self, activeEvents=None):
        pass
