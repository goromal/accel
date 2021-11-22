"""
tests.test_utils.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the accel utils modules.
"""

import pytest

import numpy as np
from accel.math.geometry import *

class TestSO3:
    """Test suite for the accel scheduler."""
    
    def test_plus_minus(self):
        np.random.seed(144440)
        R1 = SO3.random()
        w = np.array([[0.5, 0.2, 0.1]]).T
        R2 = R1 + w
        w2 = R2 - R1
        assert np.allclose(w, w2)
        
    def test_euler(self):
        roll = -1.2
        pitch = 0.6
        yaw = -0.4
        q = SO3.fromEuler(roll, pitch, yaw)
        roll2, pitch2, yaw2 = q.toEuler()
        assert np.isclose(roll, roll2) and np.isclose(pitch, pitch2) and np.isclose(yaw, yaw2)
        
class TestSE3:
    def test_plus_minus(self):
        np.random.seed(144440)
        T1 = SE3.random()
        w = np.random.random((6,1))
        T2 = T1 + w
        w2 = T2 - T1
        assert np.allclose(w, w2)
    
    def test_composition(self):
        np.random.seed(144440)
        TI = SE3.identity()
        T1 = SE3.random()
        T2 = T1 * T1.inverse()
        assert np.allclose(TI.tq(), T2.tq())
        
    def test_chart_maps(self):
        np.random.seed(144440)
        T = SE3.random()
        w = np.random.random((6,1))
        T2 = SE3.Exp(SE3.Log(T))
        assert np.allclose(T.tq(), T2.tq())
        w2 = SE3.Log(SE3.Exp(w2))
        assert np.allclose(w, w2)