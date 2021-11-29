import numpy as np
from scipy.optimize import linprog

class LinearProgram(object):
    MIN = 0
    MAX = 1
    EQ  = 2
    GEQ = 3
    LEQ = 4
    """A flexing, adaptive linear program supporting string expressions."""
    def __init__(self, numDecVars):
        pass # TODO
        # self.
        
    def setCost(self, c, type=LinearProgram.MIN):
        pass # TODO
        
    def addLinearConstraint(self, a, b, type=LinearProgram.EQ, idx=None):
        pass # TODO return success, constraintID, renderStr
        
    def addAbsConstraint(self, alpha, c, beta, type=LinearProgram.LEQ, idx=None):
        pass # TODO return success, constraintID, renderStr
        
    def rmConstraint(self, constraintID):
        pass # TODO return success
        
    def getStandard(self):
        pass # TODO return matrices (and render?)
        
    def solve(self):
        pass # TODO call getStandard, return sol stuff
    
    # TODO add analysis tools for MIT class? e.g., report on if your current program is valid, -> convert to standard form

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
        events = activeEvents if activeEvents is not None else self.events
        pass
