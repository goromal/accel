import numpy as np
import scipy
from scipy import sparse
import osqp
import accel.math.pyceres as ceres
import accel.math.geometry import SO3, SE3
import random
import string
from copy import deepcopy

# TODO https://www.geeksforgeeks.org/inner-class-in-python/

class Optimizer(object):
    class Spec(object):
        def __init__(self):
            self.valid = True
                    
        def validateArr(self, arr, size):
            if not (isinstance(arr, list) and len(arr) == size) and not (isinstance(arr, np.ndarray) and arr.size == size):
                self.valid = False
                
        def isValid(self):
            return self.valid
        
    class DecVar(Spec):
        SCALAR = 0
        SO3 = 1
        SE3 = 2
        def __init__(self, val):
            super(self, DecVar).__init__()
            self.type = None
            if isinstance(val, float):
                self.type = DecVar.SCALAR
            elif isinstance(val, SO3):
                self.type = DecVar.SO3
            elif isinstance(val, SE3):
                self.type = DecVar.SE3
            else:
                self.valid = False
            self.val = val
            
    class Cost(Spec):
        MIN = 0
        MAX = 1
        def __init__(self, parent, IDs, type):
            super(self, Cost).__init__()
            self.parent = parent
            self.IDs = list()
            self.validateIDs(IDs)
            self.type = type
            if not type == Cost.MIN and not type == Cost.MAX:
                self.valid = False
                
        def validateIDs(self, IDs):
            self.IDs.clear()
            for ID in IDs:
                self.IDs.append(ID)
                if not ID in self.parent.specs:
                    self.valid = False
                    break
          
    class LinearCost(Cost):
        def __init__(self, parent, IDs, c, type):
            super(self, LinearCost).__init__(parent, IDs, type)
            self.validateArr(c, size=len(IDs))
            
    class QuadraticCost(Cost):
        def __init__(self, parent, IDs, Q, type):
            super(self, QuadraticCost).__init__(parent, IDs, type)
            n = len(IDs)
            if not isinstance(Q, np.ndarray) or not Q.shape == (n, n):
                self.valid = False
            
    class ResidualLinearCost(Cost):
        def __init__(self, parent, IDs, a, b, type):
            super(self, ResidualLinearCost).__init__(parent, IDs, type)
            self.validateArr(a, size=len(IDs))
            if not isinstance(b, float):
                self.validate = False
            
    class ResidualSO3Cost(Cost):
        def __init__(self, parent, ID, q_meas, type):
            super(self, ResidualSO3Cost).__init__(parent, [ID], type)
            if not isinstance(q_meas, SO3):
                self.valid = False
            
    class ResidualSE3Cost(Cost):
        def __init__(self, parent, ID, T_meas, type):
            super(self, ResidualSE3Cost).__init__(parent, [ID], type)
            if not isinstance(T_meas, SE3):
                self.valid = False
            
    class Constraint(Spec):
        EQ = 0
        LEQ = 1
        GEQ = 2
        def __init__(self, parent, IDs, type):
            super(self, Constraint).__init__()
            self.parent = parent
            self.IDs = list()
            self.validateIDs(IDs)
            self.type = type
            if not type == Constraint.EQ and not type == Constraint.LEQ and not type == Constraint.GEQ:
                self.valid = False
                
        def validateIDs(self, IDs):
            self.IDs.clear()
            for ID in IDs:
                self.IDs.append(ID)
                if not ID in self.parent.specs:
                    self.valid = False
                    break
                elif not isinstance(self.parent.specs[ID], float):
                    self.valid = False
                    break

    class VariableConstraint(Constraint):
        def __init__(self, parent, ID, b, type):
            super(self, VariableConstraint).__init__(parent, [ID], type)
            if not isinstance(b, float):
                self.valid = False
            
    class LinearConstraint(Constraint):
        def __init__(self, parent, IDs, a, b, type):
            super(self, VariableConstraint).__init__(parent, IDs, type)
            self.validateArr(a, size=len(IDs))
            if not isinstance(b, float):
                self.valid = False
            
    class AbsConstraint(Constraint):
        def __init__(self, parent, ID, alpha, c, beta, type):
            super(self, AbsConstraint).__init__(parent, [ID], type)
            if not isinstance(alpha, float) or not isinstance(c, float) or not isinstance(beta, float):
                self.valid = False
                
    class Program(object):
        def __init__(self):
            self.decVarList = list()
            
        def addDecVars(self, decVars):
            pass # TODO
            
        def formulate(self):
            pass
            
        def render(self):
            return None
            
        def solve(self):
            return None
            
    class OSQProgram(Program):
        def __init__(self):
            super(OSQProgram, self).__init__()
            pass # TODO
            
        def addCosts(self, linear, quadratic, residualLinear):
            pass # TODO
            
        def addConstraints(self, variable, linear, absval):
            pass # TODO
            
        @override
        def formulate(self):
            pass # TODO
            
        @override
        def render(self):
            pass # TODO
            
        @override
        def solve(self):
            pass # TODO
            
    class CeresProgram(Program):
        def __init__(self):
            super(CeresProgram, self).__init__()
            pass # TODO
            
        def addCosts(self, linear, quadratic, residualLinear, residualSO3, residualSE3):
            pass # TODO
            
        def addConstraints(self, variable, linear, absval):
            pass # TODO
            
        @override
        def formulate(self):
            pass # TODO
            
        @override
        def render(self):
            pass # TODO
        
        @override
        def solve(self):
            pass # TODO
    
    def __init__(self):
        self.specs = dict()
        self.formulated = False
        self.program = None
    
    def _get_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    def _check_add_spec(self, spec_type, arg_tuple):
        spec = spec_type(*arg_tuple)
        specID = None
        if spec.isValid():
            specID = self._get_id()
            self.specs[specID] = spec
            self.formulated = False
        return specID
    
    def addDecVar(self, val): # Ex: x1 = opt.addDecVar(4.0)
        return self._check_add_spec(DecVar, (val))
            
    def addLinearCost(self, IDs, c, type=Cost.MIN): # Ex: C1 = opt.addLinearCost([x1, x2], [1.0, 2.0])
        return self._check_add_spec(LinearCost, (self, IDs, c, type))
        
    def addQuadraticCost(self, IDs, Q, type=Cost.MIN):
        return self._check_add_spec(QuadraticCost, (self, IDs, Q, type))
        
    def addResidualLinearCost(self, IDs, a, b, type=Cost.MIN):
        return self._check_add_spec(ResidualLinearCost, (self, IDs, a, b, type))
        
    def addResidualSO3Cost(self, ID, q_meas, type=Cost.MIN):
        return self._check_add_spec(ResidualSO3Cost, (self, ID, q_meas, type))
        
    def addResidualSE3Cost(self, ID, T_meas, type=Cost.MIN):
        return self._check_add_spec(ResidualSE3Cost, (self, ID, T_meas, type))
        
    def addVariableConstraint(self, ID, b, type):
        return self._check_add_spec(VariableConstraint, (self, ID, b, type))
        
    def addLinearConstraint(self, IDs, a, b, type):
        return self._check_add_spec(LinearConstraint, (self, IDs, a, b, type))
        
    def addAbsConstraint(self, ID, alpha, c, beta, type):
        return self._check_add_spec(AbsConstraint, (self, ID, alpha, c, beta, type))
        
    def removeSpec(self, specID):
        removed = list()
        popped = self.specs.pop(specID, None)
        if popped is not None:
            if isinstance(popped, DecVar):
                for ID, spec in self.specs.items():
                    if isinstance(spec, Cost) or isinstance(spec, Constraint):
                        dvIDs = deepcopy(spec.IDs)
                        spec.validateIDs(dvIDs)
                        if not spec.isValid():
                            removed.append(ID)
                for ID in removed:
                    del self.specs[ID]
            self.formulated = False
            removed.append(specID)
        return removed
        
    def formulate(self, render=False):
        decVars = [val for key, val in self.specs.items() if isinstance(val, DecVar)]
        linearCosts = [val for key, val in self.specs.items() if isinstance(val, LinearCost)]
        quadraticCosts = [val for key, val in self.specs.items() if isinstance(val, QuadraticCost)]
        residualLinearCosts = [val for key, val in self.specs.items() if isinstance(val, ResidualLinearCost)]
        residualSO3Costs = [val for key, val in self.specs.items() if isinstance(val, ResidualSO3Cost)]
        residualSE3Costs = [val for key, val in self.specs.items() if isinstance(val, ResidualSE3Cost)]
        variableConstraints = [val for key, val in self.specs.items() if isinstance(val, VariableConstraint)]
        linearConstraints = [val for key, val in self.specs.items() if isinstance(val, LinearConstraint)]
        absConstraints = [val for key, val in self.specs.items() if isinstance(val, AbsConstraint)]
        
        # TODO what would a joint manifold/vector optimization look like? how can we facilitate it?
        
        if len(residualSO3Costs) == 0 and len(residualSE3Costs) == 0:
            self.program = OSQProgram()
            self.program.addDecVars(decVars)
            self.program.addCosts(linearCosts, quadraticCosts, residualLinearCosts)
            self.program.addConstraints(variableConstraints, linearConstraints, absConstraints)
        else:
            self.program = CeresProgram()
            self.program.addDecVars(decVars)
            self.program.addCosts(linearCosts, quadraticCosts, residualLinearCosts, residualSO3Costs, residualSE3Costs)
            self.program.addConstraints(variableConstraints, linearConstraints, absConstraints)
            
        self.program.formulate()
        self.formulated = True
        
    def render(self):
        if not self.formulated:
            self.formulate()
        return self.program.render()
        
    def solve(self):
        if not self.formulated:
            self.formulate()
        return self.program.solve()
            
            
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
        
class LineFitter(object):
    pass # TODO
    
class RotationAverager(object):
    pass # TODO
    
class TransformAverager(object):
    pass # TODO
    
class PGO(object):
    pass # TODO
