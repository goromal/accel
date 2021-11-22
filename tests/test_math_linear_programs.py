"""
tests.test_utils.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the accel utils modules.
"""

# from copy import deepcopy

import pytest

# from py_pkg.curves import (SupplyCurve, DemandCurve, Equilibrium,
#                            SupplyMonotonicityError, DemandMonotonicityError,
#                            equil_price, equil_price_ranges, HorizPriceShock,
#                            PriceRanges)

class TestScheduler:
    """Test suite for the accel scheduler."""
    
    def test_simple_linear(self):
        """Test a simple linear scheduling problem."""
        assert True # TODO
        
    def test_impossible_cycle(self):
        """Test an impossible scheduling problem."""
        assert True # TODO

"""
class TestSupplyCurve:
    
    def test_curve_comparison(self, supply_curve: SupplyCurve):
        assert supply_curve == deepcopy(supply_curve)

    def test_curve_points(self, supply_curve: SupplyCurve):
        price = 8000
        quantity = 3
        assert supply_curve.quantity(price) == quantity

    def test_curve_interpolation(self, supply_curve: SupplyCurve):
        price = 9500
        quantity = 3
        assert supply_curve.quantity(price) == quantity

    def test_curve_extrapolation_from_above(self, supply_curve: SupplyCurve):
        price = 13000
        quantity = 6
        assert supply_curve.quantity(price) == quantity

    def test_curve_extrapolation_from_below(self, supply_curve: SupplyCurve):
        price = 5000
        quantity = 0
        assert supply_curve.quantity(price) == quantity

    def test_curve_raises_monotonicity_exception(self):
        supply_data = [
            {"price": 7000, "supply": 1},
            {"price": 8000, "supply": 3},
            {"price": 9000, "supply": 3},
            {"price": 10000, "supply": 2},
            {"price": 11000, "supply": 6},
            {"price": 12000, "supply": 6}]

        with pytest.raises(SupplyMonotonicityError):
            SupplyCurve(supply_data)

    def test_curve_raises_zero_price_exception(self):
        supply_data = [
            {"price": 0, "supply": 1}]

        with pytest.raises(ValueError):
            SupplyCurve(supply_data)


class TestDemandCurve:
    
    def test_curve_comparison(self, demand_curve: DemandCurve):
        assert demand_curve == deepcopy(demand_curve)

    def test_curve_points(self, demand_curve: DemandCurve):
        price = 8000
        quantity = 10
        assert demand_curve.quantity(price) == quantity

    def test_curve_interpolation(self, demand_curve: DemandCurve):
        price = 9500
        quantity = 3
        assert demand_curve.quantity(price) == quantity

    def test_curve_extrapolation_from_above(self, demand_curve: DemandCurve):
        price = 13000
        quantity = 0
        assert demand_curve.quantity(price) == quantity

    def test_curve_extrapolation_from_below(self, demand_curve: DemandCurve):
        price = 5000
        quantity = 15
        assert demand_curve.quantity(price) == quantity

    def test_curve_raises_monotonicity_exception(self):
        demand_data = [
                {"price": 7000, "demand": 15},
                {"price": 8000, "demand": 10},
                {"price": 9000, "demand": 5},
                {"price": 10000, "demand": 3},
                {"price": 11000, "demand": 2},
                {"price": 12000, "demand": 3}]

        with pytest.raises(DemandMonotonicityError):
            DemandCurve(demand_data)

    def test_curve_raises_zero_price_exception(self):
        demand_data = [
            {"price": 0, "demand": 1}]

        with pytest.raises(ValueError):
            DemandCurve(demand_data)


class TestCurveAnalytics:
    
    def test_equilibrium_price(self, supply_curve: SupplyCurve, 
                               demand_curve: DemandCurve):
        assert equil_price(supply_curve, demand_curve) == 9000

    def test_equilibrium_price_ranges(self, supply_curve: SupplyCurve,
                                      demand_curve: DemandCurve):
        assert (equil_price_ranges(supply_curve, demand_curve)
                == PriceRanges((8000, 9000), (9000, 10000)))

    def test_horiz_supply_shock(self, supply_curve: SupplyCurve):
        econ_shock = HorizPriceShock(supply_shock=1500)
        shifted_supply_curve = econ_shock.apply(supply_curve)
        price_diffs = shifted_supply_curve._price - supply_curve._price
        assert price_diffs == pytest.approx(econ_shock.supply_shock)
        assert isinstance(shifted_supply_curve, SupplyCurve)

    def test_horiz_demand_shock(self, demand_curve: DemandCurve):
        econ_shock = HorizPriceShock(demand_shock=1500)
        shifted_demand_curve = econ_shock.apply(demand_curve)
        price_diffs = shifted_demand_curve._price - demand_curve._price
        assert price_diffs == pytest.approx(econ_shock.demand_shock)
        assert isinstance(shifted_demand_curve, DemandCurve)

    def test_equilibrium(self, supply_curve: SupplyCurve, 
                         demand_curve: DemandCurve):
        equilibrium = Equilibrium(supply_curve, demand_curve)
        assert equilibrium.price == 9000
        assert (equilibrium.price_ranges
                == PriceRanges((8000, 9000), (9000, 10000)))
        assert equilibrium.supply_q == 3
        assert equilibrium.demand_q == 5

    def test_equilibrium_comparison(self, supply_curve: SupplyCurve, 
                                    demand_curve: DemandCurve):
        assert (Equilibrium(supply_curve, demand_curve)
                == Equilibrium(supply_curve, demand_curve))
"""