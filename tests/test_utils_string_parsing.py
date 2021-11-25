import pytest
from accel.utils.string_parsing import hhmmss_from_str

class TestStringParsing:
    def test_time_parsing(self):
        assert hhmmss_from_str('0:1') == (0,0,1.0)
        assert hhmmss_from_str('2:00:1') == (2,0,1.0)
        assert hhmmss_from_str('03:04:1.98') == (3,4,1.98)
        assert hhmmss_from_str('4:5.987') == (0,4,5.987)
        assert hhmmss_from_str('00:00') == (0,0,0.0)