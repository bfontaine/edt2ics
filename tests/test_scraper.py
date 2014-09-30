# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from helpers import noop

from edt2ics.scraper import ScheduleScraper

class TestScraper(unittest.TestCase):

    def setUp(self):
        self._fetch_mth = ScheduleScraper._fetch
        ScheduleScraper._fetch = noop


    def tearDown(self):
        ScheduleScraper._fetch = self._fetch_mth


    # __init__

    def test_init_with_year(self):
        year = 'L3'
        s = ScheduleScraper(year=year)
        self.assertEquals(year, s.year)

