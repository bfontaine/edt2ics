# -*- coding: UTF-8 -*-

from datetime import date, time
from icalendar import Calendar

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


    def setUp(self):
        self.ev = {
            'day': 1,
            'tstart': time(10, 30),
            'tend': time(11, 30),
            'type_': 'cours',
            'title': 'Foo',
            'room': '9 3/4',
            'description': '...'}

    # __init__

    def test_init_without_events(self):
        ics = iCalSchedule(FakeScraper(events=[]))
        self.assertEquals(0, len(list(ics.cal.subcomponents)))

    def test_init_with_events(self):
        ics = iCalSchedule(FakeScraper(events=[self.ev]))
        self.assertEquals(1, len(list(ics.cal.subcomponents)))

    # _init_ical

    def test_init_ical_set_properties(self):
        ics = iCalSchedule(FakeScraper())
        self.assertSequenceEqual(['VERSION', 'PRODID', 'METHOD'],
                list(ics.cal.keys()))

    # _recur_params

    def test_recur_params_week_start_on_monday(self):
        ics = iCalSchedule(FakeScraper())
        self.assertEquals('MO', ics._recur_params(4)['wkst'])

    def test_recur_params_until_enddate_plus_one_day(self):
        d1 = date(2014, 10, 2)
        d2 = date(2014, 10, 3)
        ics = iCalSchedule(FakeScraper(), enddate=d1)
        params = ics._recur_params(2)
        self.assertEquals(d2, params['until'])

    # _get_dates

    # _str2date

    def test_str2date_correct_date(self):
        ics = iCalSchedule(FakeScraper())
        d1 = date(2014, 9, 30)
        d2 = ics._str2date('%d-%d-%d' % (d1.year, d1.month, d1.day))
        self.assertEquals(d1, d2)

    def test_str2date_incorrect_date_raises_exception(self):
        ics = iCalSchedule(FakeScraper())
        self.assertRaises(ValueError, lambda: ics._str2date('2014-02-30'))


    # add_event

    def test_add_event_set_uid(self):
        ics = iCalSchedule(FakeScraper())
        ics.add_event(ScheduleEvent(**self.ev))
        ev = ics.cal.subcomponents[0]
        self.assertIn('UID', ev.keys())


    # to_ical

    def test_to_ical(self):
        ics = iCalSchedule(FakeScraper(events=[self.ev]))
        cal1 = ics.cal
        cal2 = Calendar.from_ical(ics.to_ical())
        self.assertEquals(cal1, cal2)
