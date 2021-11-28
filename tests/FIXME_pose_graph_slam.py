import PyCeres
import numpy as np
from rotations import *
from transforms import *

##
# Pose Graph SLAM
##

# odom, loop closure covariances (linear, angular)
odom_cov_vals = (0.5, 0.01)
lc_cov_vals = (0.001, 0.0001)

# simulation parameters
num_steps = 50
num_lc = 12

# delta pose/odometry between successive nodes in graph (tangent space representation as a local perturbation)
dx = np.array([[1.,0.,0.,0.,0.,0.1]]).T

# odometry covariance
odom_cov = np.eye(6)
odom_cov[:3,:3] *= odom_cov_vals[0] # delta translation noise
odom_cov[3:,3:] *= odom_cov_vals[1] # delta rotation noise
odom_cov_sqrt = np.linalg.cholesky(odom_cov)

# loop closure covariance
lc_cov = np.eye(6)
lc_cov[:3,:3] *= lc_cov_vals[0] # relative translation noise
lc_cov[3:,3:] *= lc_cov_vals[1] # relative rotation noise
lc_cov_sqrt = np.linalg.cholesky(lc_cov)

# truth/estimate buffers
x = list()
xhat = list() # need to keep parameter arrays separate (only in Python) to prevent memory aliasing

# determine which pose indices will have loop closures between them
loop_closures = list()
for l in range(num_lc):
    i = np.random.randint(low=0, high=num_steps-1)
    j = np.random.randint(low=0, high=num_steps-2)
    if j == i:
        j = num_steps-1
    loop_closures.append((i,j))

# optimization problem
problem = PyCeres.Problem()

# create odometry measurements
for k in range(num_steps):
    if k == 0:
        # starting pose
        xhat.append(SE3.identity().array())
        x.append(SE3.identity().array())

        # add (fixed) prior to the graph
        problem.AddParameterBlock(xhat[k], 7, PyCeres.SE3Parameterization())
        problem.SetParameterBlockConstant(xhat[k])
    else:
        # time step endpoints
        i = k-1
        j = k

        # simulate system
        x.append((SE3(x[i].reshape((7,1))) + dx)).array()

        # create noisy front-end measurement (constrained to the horizontal plane)
        dx_noise = odom_cov_sqrt.dot(np.random.normal(np.zeros((6,1)), np.ones((6,1)), (6,1)))
        dx_noise[2,0] = dx_noise[3,0] = dx_noise[4,0] = 0.
        dxhat = SE3.Exp(dx + dx_noise)
        xhat.append((SE3(xhat[i].reshape((7,1))) * dxhat).array())

        # add relative measurement to the problem as a between factor (with appropriate parameterization)
        problem.AddParameterBlock(xhat[j], 7, PyCeres.SE3Parameterization())
        problem.AddResidualBlock(PyCeres.SE3Factor(dxhat.array(), odom_cov), None, xhat[i], xhat[j])

# create loop closure measurements
for l in range(num_lc):
    i = loop_closures[l][0]
    j = loop_closures[l][1]

    # noise-less loop closure measurement
    xi = SE3(x[i].reshape((7,1)))
    xj = SE3(x[j].reshape((7,1)))
    xij = SE3.Exp(xj - xi)

    # add noise to loop closure measurement (constrained to the horizontal plane)
    dx_noise = lc_cov_sqrt.dot(np.random.normal(np.zeros((6,1)), np.ones((6,1)), (6,1)))
    dx_noise[2,0] = dx_noise[3,0] = dx_noise[4,0] = 0.

    dx_meas = xij + dx_noise

    # add relative measurement to the problem as a between factor
    problem.AddResidualBlock(PyCeres.SE3Factor(dx_meas.array(), lc_cov), None, xhat[i], xhat[j])

# initial error, for reference
prev_err = 0.
for k in range(num_steps):
    prev_err += 1.0/6.0*np.linalg.norm(x[k] - xhat[k])**2
prev_err /= num_steps

# set solver options
options = PyCeres.SolverOptions()
options.max_num_iterations = 25
options.linear_solver_type = PyCeres.LinearSolverType.SPARSE_NORMAL_CHOLESKY
options.minimizer_progress_to_stdout = True

# solve!
summary = PyCeres.Summary()
PyCeres.Solve(options, problem, summary)

# report results
post_err = 0.
for k in range(num_steps):
    post_err += 1.0/6.0*np.linalg.norm(x[k] - xhat[k])**2
post_err /= num_steps
print('Average error of optimized poses: %f -> %f' % (prev_err, post_err))