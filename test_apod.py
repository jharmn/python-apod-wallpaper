import unittest
from datetime import date
from apod_wallpaper import apod, date_utils

class DatesTestCase(unittest.TestCase):
    def test_format_date(self):
        sdate = date_utils.format_date(date(2015, 7, 25))
        assert sdate == '2015-07-25'

    def test_date_range(self):
        start = date(2015, 7, 25)
        end = date(2015, 7, 26)
        r = date_utils.date_range(start, end)
        for d in r:
            assert start <= d <= end

    def test_random_date(self):
        start = date(2015, 7, 25)
        end = date(2015, 7, 26)
        r = date_utils.random_date(start, end)
        assert start <= r <= end

if __name__ == "__main__":
    unittest.main()
