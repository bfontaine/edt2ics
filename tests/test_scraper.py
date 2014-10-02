# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from bs4 import BeautifulSoup
from datetime import date, time

from helpers import noop

from edt2ics.scraper import ScheduleScraper


class TestScraper(unittest.TestCase):

    def setUp(self):
        self._fetch_mth = ScheduleScraper._fetch
        ScheduleScraper._fetch = noop

    def tearDown(self):
        ScheduleScraper._fetch = self._fetch_mth

    def mk_fake_fetch(filename):
        def _fetch(self):
            stream = open(filename, 'r')
            self._soup = BeautifulSoup(stream, 'lxml')
        return _fetch

    def mk_fake_source(self, filename):
        """
        Mock ScheduleScraper to use a file source instead of a remote URL
        """
        ScheduleScraper._fetch = self.mk_fake_fetch(filename)


    # __init__

    def test_init_with_year(self):
        year = 'L3'
        s = ScheduleScraper(year=year)
        self.assertEquals(year, s.year)


    # _guess_period

    def test_guess_period_first_semester(self):
        s = ScheduleScraper('M1')
        period = s._guess_period(today=date(2014, 9, 1))
        self.assertEquals('2014-2015', period)

    def test_guess_period_second_semester(self):
        s = ScheduleScraper('M1')
        period = s._guess_period(today=date(2014, 3, 1))
        self.assertEquals('2013-2014', period)


    # parse_day
    # _parse_hm

    def test_parse_hm_no_minutes(self):
        s = ScheduleScraper('M1')
        seq = s._parse_hm('23h')
        self.assertSequenceEqual([23, 0], seq)

    def test_parse_hm_minutes(self):
        s = ScheduleScraper('M1')
        seq = s._parse_hm('13h37')
        self.assertSequenceEqual([13, 37], seq)

    # parse_time

    def test_parse_time_no_minutes(self):
        s = ScheduleScraper('M1')
        seq = s.parse_time('11h')
        self.assertEquals(time(11, 0), seq)

    def test_parse_time_minutes(self):
        s = ScheduleScraper('M1')
        seq = s.parse_time('11h17')
        self.assertEquals(time(11, 17), seq)

    # parse_type
