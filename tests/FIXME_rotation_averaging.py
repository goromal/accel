import PyCeres
import numpy as np
from rotations import *

##
# Rotation Averaging with Quaternions
##

# number of rotations to average over
N = 1000
# scaling factor for noisy rotations
noise_scale = 1e-2

# true average quaternion
q = SO3.random()
# decision vector form of q
x = q.array()

# initial vector guess for average quaternion
xhat = SO3.identity().array()

# optimization problem with SO(3) local parameterization
problem = PyCeres.Problem()
problem.AddParameterBlock(xhat, 4, PyCeres.SO3Parameterization())

# create noisy rotations around the true average and add to problem as 
# measurement residuals
for i in range(N):
    sample = (q + np.random.rand(3,1) * noise_scale).array()
    problem.AddResidualBlock(PyCeres.SO3Factor(sample),
                             None,
                             xhat)

# set solver options
options = PyCeres.SolverOptions()
options.max_num_iterations = 25
options.linear_solver_type = PyCeres.LinearSolverType.DENSE_QR
options.minimizer_progress_to_stdout = True

# solve!
summary = PyCeres.Summary()
PyCeres.Solve(options, problem, summary)

# report results
q_hat = SO3(xhat.reshape((4,1)))
print('q:', q)
print('q_hat:', q_hat)