import numpy as np
import accel.math.pyceres as ceres

""" linalg -> osqp -> pyceres
linalg:
min  r^Tr
s.t. r = Ax - b

osqp:
min  r^Tr
"""

# TODO