#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import date, datetime, timedelta
from icalendar import Calendar, Event, vRecur
import json
import os.path
from os.path import dirname
from uuid import uuid4


class iCalSchedule(object):

    DAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']

    def __init__(self, scraper, startdate=None, enddate=None):
        if startdate is None or enddate is None:
            dts, dte = self._get_dates(scraper.period, scraper.year,
                    scraper.semester)

            if startdate is None:
                startdate = dts
            if enddate is None:
                enddate = dte

        self.startdate = startdate
        # The 'DTEND' property is exclusive, we then must end one day later
        self.enddate = enddate + timedelta(days=1)
        self._first_weekdays = {} # cache
        self._init_ical()
        for ev in scraper.get_events():
            self.add_event(ev)


    def _init_ical(self):
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//edt2ics//bfontaine.net//')
        cal.add('method', 'publish')
        self.cal = cal


    def _recur_params(self, wday):
        return {
            'freq': 'weekly',
            'wkst': self.DAYS[0],
            'byday': self.DAYS[wday],
            'until': self.enddate,
        }


    def _get_first_weekday(self, day):
        """
        Return the first date after ``self.startdate`` which is on the given
        weekday (0=Monday, 1=Tuesday, etc)
        """
        if day not in self._first_weekdays:
            start_wd = self.startdate.weekday()
            delta = (day - start_wd + 7) % 7
            self._first_weekdays[day] = self.startdate + timedelta(days=delta)
        return self._first_weekdays[day]


    def _get_dates(self, period, year, semester):
        source = os.path.join(dirname(__file__), 'dates.json')
        with open(source, 'r') as f:
            data = json.loads(f.read())
        dates = data['dates'][period][str(semester)][year]
        start, end = dates['start'], dates['end']

        return self._str2date(start), self._str2date(end)


    def _str2date(self, s):
        return date(*map(lambda e: int(e, 10), s.split('-')))


    def add_event(self, ev):
        """
        Add a new recurrent event to this schedule
        """
        day = self._get_first_weekday(ev.day)
        dtstart = datetime.combine(day, ev.tstart)
        dtend = datetime.combine(day, ev.tend)

        tz_params = {'tzid': 'Europe/Paris'}

        iev = Event()
        iev.add('uid', str(uuid4()))
        iev.add('status', 'confirmed')
        iev.add('dtstart', dtstart, parameters=tz_params)
        iev.add('dtend', dtend, parameters=tz_params)
        iev.add('rrule', vRecur(self._recur_params(ev.day)))
        iev.add('summary', '%s %s' % (ev.type_, ev.title))
        iev.add('location', ev.room)
        iev.add('description', ev.description)
        self.cal.add_component(iev)


    def to_ical(self):
        return self.cal.to_ical()
