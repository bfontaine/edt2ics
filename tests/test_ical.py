# -*- coding: UTF-8 -*-

from datetime import date
from tempfile import NamedTemporaryFile
from os import remove

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from edt2ics.events import ScheduleEvent
from edt2ics.ical import iCalSchedule

class FakeScraper(object):

    def __init__(self, events=[], period='2014-2015', year='M1', semester=1):
        self.period = period
        self.year = year
        self.semester = semester
        self._events = events

    def get_events(self):
        for ev in self._events:
            yield ScheduleEvent(**ev)



class TestICal(unittest.TestCase):

    # _str2date

    def test_str2date_correct_date(self):
        ics = iCalSchedule(FakeScraper())
        d1 = date(2014, 9, 30)
        d2 = ics._str2date('%d-%d-%d' % (d1.year, d1.month, d1.day))
        self.assertEquals(d1, d2)
