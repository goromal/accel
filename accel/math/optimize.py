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
        def __init__(self, val, fixed):
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
            self.fixed = fixed
            
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
            self.c = c
            
    class QuadraticCost(Cost):
        def __init__(self, parent, IDs, Q, type):
            super(self, QuadraticCost).__init__(parent, IDs, type)
            n = len(IDs)
            if not isinstance(Q, np.ndarray) or not Q.shape == (n, n):
                self.valid = False
            self.Q = Q
            
    class ResidualLinearCost(Cost):
        def __init__(self, parent, IDs, a, b, type):
            super(self, ResidualLinearCost).__init__(parent, IDs, type)
            self.validateArr(a, size=len(IDs))
            if not isinstance(b, float):
                self.validate = False
            self.a = a
            self.b = b
            
    class ResidualSO3Cost(Cost):
        def __init__(self, parent, ID, q_meas, Q, type):
            super(self, ResidualSO3Cost).__init__(parent, [ID], type)
            if not isinstance(q_meas, SO3):
                self.valid = False
            if not isinstance(Q, np.ndarray) or Q.shape != (3, 3):
                self.valid = False
            self.q = q_meas.array()
            self.Q = Q
            
    class ResidualDeltaSO3Cost(Cost):
        def __init__(self, parent, IDi, IDj, qij_meas, Q, type):
            super(self, ResidualDeltaSO3Cost).__init__(parent, [IDi, IDj], type)
            if not isinstance(qij_meas, SO3):
                self.valid = False
            if not isinstance(Q, np.ndarray) or Q.shape != (3, 3):
                self.valid = False
            self.q = qij_meas.array()
            self.Q = Q
            
    class ResidualSE3Cost(Cost):
        def __init__(self, parent, ID, T_meas, Q, type):
            super(self, ResidualSE3Cost).__init__(parent, [ID], type)
            if not isinstance(T_meas, SE3):
                self.valid = False
            if not isinstance(Q, np.ndarray) or Q.shape != (6, 6):
                self.valid = False
            self.T = T_meas.array()
            self.Q = Q
            
    class ResidualDeltaSE3Cost(Cost):
        def __init__(self, parent, IDi, IDj, Tij_meas, Q, type):
            super(self, ResidualDeltaSE3Cost).__init__(parent, [IDi, IDj], type)
            if not isinstance(Tij_meas, SE3):
                self.valid = False
            if not isinstance(Q, np.ndarray) or Q.shape != (6, 6):
                self.valid = False
            self.T = Tij_meas.array()
            self.Q = Q
            
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
            self.b = b
            
    class LinearConstraint(Constraint):
        def __init__(self, parent, IDs, a, b, type):
            super(self, VariableConstraint).__init__(parent, IDs, type)
            self.validateArr(a, size=len(IDs))
            if not isinstance(b, float):
                self.valid = False
            self.a = a
            self.b = b
            
    class AbsConstraint(Constraint):
        def __init__(self, parent, ID, alpha, c, beta, type):
            super(self, AbsConstraint).__init__(parent, [ID], type)
            if not isinstance(alpha, float) or not isinstance(c, float) or not isinstance(beta, float):
                self.valid = False
            self.a = alpha
            self.b = beta
            self.c = c
                
    class Program(object):
        def __init__(self, decVars):
            self.decVarLabels = list()
            self.decVarTypes = list()
            self.decVarFixed = list()
            self.decVarList = list()
            for key, decVar in decVars:
                self.decVarLabels.append(key)
                self.decVarTypes.append(decVar.type)
                self.decVarFixed.append(decVar.fixed)
                if decVar.type == DecVar.SCALAR:
                    self.decVarList.append(decVal.val)
                else:
                    self.decVarList.append(decVal.val.array())
                    
        def _get_decvar(self, key):
            return self.decVarList[self.decVarLabels.index(key)]
            
        def render(self):
            return None
        
        def solve(self):
            return None
            
    class OSQProgram(Program):
        def __init__(self, decVars):
            super(OSQProgram, self).__init__(decVars)
            allScalars = True
            for type in self.decVarTypes:
                allScalars = allScalars and (type == DecVar.SCALAR)
            assert allScalars
            self.n = len(self.decVarList)
            self.m = 0
            self.P = np.zeros((self.n, self.n))
            self.q = np.zeros((self.n,))
            self.A = None
            self.l = None
            self.u = None
            self.Arows = list()
            self.lrows = list()
            self.urows = list()
            
        def addCosts(self, linear, quadratic, residualLinear):
            pass # TODO
            
        def addConstraints(self, variable, linear, absval):
            pass # TODO
            
        def createMatrices(self):
            if self.m > 0:
                self.A = np.vstack(self.Arows)
                self.l = np.array(self.lrows)
                self.u = np.array(self.urows)
            
        @override
        def render(self):
            if self.A is None:
                self.createMatrices()
            raise NotImplementedError
            
        @override
        def solve(self):
            if self.A is None:
                self.createMatrices()
            # TODO make P and A sparse matrices
            prob = osqp.OSQP()
            prob.setup(self.P, self.q, self.A, self.l, self.u)
            res = prob.solve()
            pass # TODO
            
    class CeresProgram(Program):
        def __init__(self, decVars):
            super(CeresProgram, self).__init__(decVars)
            self.problem = ceres.Problem()
            self.options = ceres.SolverOptions()
            self.options.max_num_iterations = 25
            self.options.linear_solver_type = ceres.LinearSolverType.SPARSE_NORMAL_CHOLESKY
            self.options.minimizer_progress_to_stdout = False
            self.summary = ceres.Summary()
            for i in range(len(self.decVarList)):
                if self.decVarTypes[i] == DecVar.SCALAR:
                    raise NotImplementedError
                elif self.decVarTypes[i] == DecVar.SO3:
                    self.problem.AddParameterBlock(self.decVarList[i], 4, ceres.SO3Parameterization())
                elif self.decVarTypes[i] == DecVar.SE3:
                    self.problem.AddParameterBlock(self.decVarList[i], 7, ceres.SE3Parameterization())
                else:
                    raise NotImplementedError
                if self.decVarFixed[i]:
                    self.problem.SetParameterBlockConstant(self.decVarList[i])
            
        def addCosts(self, linear, quadratic, residualLinear, residualSO3, residualDeltaSO3, residualSE3, residualDeltaSE3):
            for cost in linear:
                raise NotImplementedError
            for cost in quadratic:
                raise NotImplementedError
            for cost in residualLinear:
                raise NotImplementedError
            for cost in residualSO3:
                self.problem.AddResidualBlock(ceres.SO3Factor(cost.q, cost.Q), None, self._get_decvar(cost.IDs[0]))
            for cost in residualDeltaSO3:
                self.problem.AddResidualBlock(ceres.DeltaSO3Factor(cost.q, cost.Q), None, self._get_decvar(cost.IDs[0]), self._get_decvar(cost.IDs[1]))
            for cost in residualSE3:
                self.problem.AddResidualBlock(ceres.SE3Factor(cost.T, cost.Q), None, self._get_decvar(cost.IDs[0]))
            for cost in residualDeltaSE3:
                self.problem.AddResidualBlock(ceres.DeltaSE3Factor(cost.T, cost.Q), None, self._get_decvar(cost.IDs[0]), self._get_decvar(cost.IDs[1]))
            
        def addConstraints(self, variable, linear, absval):
            for cons in variable:
                raise NotImplementedError
            for cons in linear:
                raise NotImplementedError
            for cons in absval:
                raise NotImplementedError
            
        @override
        def render(self):
            raise NotImplementedError
        
        @override
        def solve(self):
            ceres.Solve(self.options, self.problem, self.summary)
            solved = self.summary.IsSolutionUsable()
            sols = list()
            for label, type, val in zip(self.decVarLabels, self.decVarTypes, self.decVarList):
                sol = None
                if type == DecVar.SCALAR:
                    sol = val
                elif type == DecVar.SO3:
                    sol = SO3(val)
                elif type == DecVar.SE3:
                    sol = SE3(val)
                sols.append((label, sol))
            return solved, sols
    
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
    
    def addDecVar(self, val, fixed=False): # Ex: x1 = opt.addDecVar(4.0)
        return self._check_add_spec(DecVar, (val, fixed))
            
    def addLinearCost(self, IDs, c, type=Cost.MIN): # Ex: C1 = opt.addLinearCost([x1, x2], [1.0, 2.0])
        return self._check_add_spec(LinearCost, (self, IDs, c, type))
        
    def addQuadraticCost(self, IDs, Q, type=Cost.MIN):
        return self._check_add_spec(QuadraticCost, (self, IDs, Q, type))
        
    def addResidualLinearCost(self, IDs, a, b, type=Cost.MIN):
        return self._check_add_spec(ResidualLinearCost, (self, IDs, a, b, type))
        
    def addResidualSO3Cost(self, ID, q_meas, Q=np.eye((3,3))):
        return self._check_add_spec(ResidualSO3Cost, (self, ID, q_meas, Q, Cost.MIN))
        
    def addResidualDeltaSO3Cost(self, IDi, IDj, qij_meas, Q=np.eye((3,3))):
        return self._check_add_spec(ResidualDeltaSO3Cost, (self, IDi, IDj, qij_meas, Q, Cost.MIN))
        
    def addResidualSE3Cost(self, ID, T_meas, Q=np.eye((6,6))):
        return self._check_add_spec(ResidualSE3Cost, (self, ID, T_meas, Q, Cost.MIN))
        
    def addResidualDeltaSE3Cost(self, IDi, IDj, Tij_meas, Q=np.eye((6,6))):
        return self._check_add_spec(ResidualDeltaSE3Cost, (self, IDi, IDj, Tij_meas, Q, Cost.MIN))
        
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
        decVars = [(key, val) for key, val in self.specs.items() if isinstance(val, DecVar)]
        linearCosts = [val for key, val in self.specs.items() if isinstance(val, LinearCost)]
        quadraticCosts = [val for key, val in self.specs.items() if isinstance(val, QuadraticCost)]
        residualLinearCosts = [val for key, val in self.specs.items() if isinstance(val, ResidualLinearCost)]
        residualSO3Costs = [val for key, val in self.specs.items() if isinstance(val, ResidualSO3Cost)]
        residualDeltaSO3Costs = [val for key, val in self.specs.items() if isinstance(val, ResidualDeltaSO3Cost)]
        residualSE3Costs = [val for key, val in self.specs.items() if isinstance(val, ResidualSE3Cost)]
        residualDeltaSE3Costs = [val for key, val in self.specs.items() if isinstance(val, ResidualDeltaSE3Cost)]
        variableConstraints = [val for key, val in self.specs.items() if isinstance(val, VariableConstraint)]
        linearConstraints = [val for key, val in self.specs.items() if isinstance(val, LinearConstraint)]
        absConstraints = [val for key, val in self.specs.items() if isinstance(val, AbsConstraint)]
        
        # TODO what would a joint manifold/vector optimization look like? how can we facilitate it?
        
        if len(residualSO3Costs) == 0 and len(residualSE3Costs) == 0 and len(residualDeltaSO3Costs) == 0 and len(residualDeltaSE3Costs) == 0:
            self.program = OSQProgram(decVars)
            self.program.addCosts(linearCosts, quadraticCosts, residualLinearCosts)
            self.program.addConstraints(variableConstraints, linearConstraints, absConstraints)
            self.program.createMatrices()
        else:
            self.program = CeresProgram(decVars)
            self.program.addCosts(linearCosts, quadraticCosts, residualLinearCosts, residualSO3Costs, residualDeltaSO3Costs, residualSE3Costs, residualDeltaSE3Costs)
            self.program.addConstraints(variableConstraints, linearConstraints, absConstraints)
            
        self.formulated = True
        
    def render(self):
        if not self.formulated:
            self.formulate()
        return self.program.render()
        
    def solve(self):
        if not self.formulated:
            self.formulate()
        return self.program.solve()
            
            
class Scheduler(object): # TODO refactor
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
    pass # TODO accommodate options for lasso and huber fitting
    
class KinematicMPC(object):
    pass # TODO up to n derivatives, should provide great intuition
    
class RiskAdjustedReturn(object):
    pass # TODO call stats methods?
    
class BinaryClassifier(object):
    pass # TODO
    
class RotationAverager(object):
    pass # TODO
    
class TransformAverager(object):
    pass # TODO
    
class PGO(object):
    pass # TODO
