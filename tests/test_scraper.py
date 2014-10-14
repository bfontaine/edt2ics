# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from bs4 import BeautifulSoup
from datetime import date, time
import os.path

from helpers import noop

from edt2ics.scraper import ScheduleScraper


class TestScraper(unittest.TestCase):

    def setUp(self):
        self._fetch_mth = ScheduleScraper._fetch
        ScheduleScraper._fetch = noop
        self.scraper = ScheduleScraper('M1')

    def tearDown(self):
        ScheduleScraper._fetch = self._fetch_mth

    def mk_fake_fetch(self, filename):
        def _fetch(self):
            "fake fetch"
            path = '%s/samples/%s' % (os.path.dirname(__file__), filename)
            self._soup = BeautifulSoup(open(path), 'lxml')
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
        period = self.scraper._guess_period(today=date(2014, 9, 1))
        self.assertEquals('2014-2015', period)

    def test_guess_period_second_semester(self):
        period = self.scraper._guess_period(today=date(2014, 3, 1))
        self.assertEquals('2013-2014', period)


    # get_events

    def test_get_no_events(self):
        self.scraper._soup = BeautifulSoup('')
        self.assertEquals([], list(self.scraper.get_events()))

    def test_get_events_sample_M1(self):
        self.mk_fake_source('2014-2015-1-M1.html')
        s = ScheduleScraper('M1')
        self.assertEquals(28, len(list(s.get_events())))

    def test_get_events_sample_error(self):
        self.mk_fake_source('2014-2015-2-L1-error.html')
        s = ScheduleScraper('M1')
        self.assertEquals([], list(s.get_events()))


    # parse_day

    def test_parse_day_none(self):
        self.assertIs(self.scraper.parse_day(None), None)

    def test_parse_wrong_day(self):
        self.assertIs(self.scraper.parse_day('Manchedi'), None)

    def test_parse_day(self):
        day = self.scraper.DAYS[2]
        self.assertIs(self.scraper.parse_day(day), 2)

    # _parse_hm

    def test_parse_hm_no_minutes(self):
        seq = self.scraper._parse_hm('23h')
        self.assertSequenceEqual([23, 0], seq)

    def test_parse_hm_minutes(self):
        seq = self.scraper._parse_hm('13h37')
        self.assertSequenceEqual([13, 37], seq)

    # parse_time

    def test_parse_time_no_minutes(self):
        seq = self.scraper.parse_time('11h')
        self.assertEquals(time(11, 0), seq)

    def test_parse_time_minutes(self):
        seq = self.scraper.parse_time('11h17')
        self.assertEquals(time(11, 17), seq)

    # parse_type

    def test_parse_capitalized_type(self):
        t = 'Cqzoer1'
        self.assertEquals(t, self.scraper.parse_type(t))

    def test_parse_capitalized_type_year(self):
        t = 'Cqzoer1'
        self.assertEquals(t, self.scraper.parse_type('%s_M1' % t))

    def test_parse_type_long_str(self):
        t = 'cqzoer1artos23q'
        self.assertEquals(t.capitalize(), self.scraper.parse_type(t))

    def test_parse_type_empty_str(self):
        self.assertEquals('', self.scraper.parse_type(''))

    def test_parse_type_tp(self):
        self.assertEquals('TP', self.scraper.parse_type('tp'))
        self.assertEquals('TP', self.scraper.parse_type('Tp'))
        self.assertEquals('TP', self.scraper.parse_type('TP'))

    def test_parse_type_strip(self):
        self.assertEquals('TP', self.scraper.parse_type('tp    '))
        self.assertEquals('TP', self.scraper.parse_type(' tp   '))
